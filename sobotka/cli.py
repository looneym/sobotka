from sys import exit
import argparse
import os 
import datetime

import yaml
import pytz

import db
from models import Project 
from aws import Ec2Manager, KeyPairManager
from remote_command_runner import RemoteCommandRunner 
from file_sync_utility import FileSyncUtility
from hosts_file_manager import HostsFileManager
from ssh_config_file_manager import SshConfigFileManager

##
## 
## LOCAL CONF & MANIFEST
##
##

def load_local_conf():
    try:
        return yaml.safe_load(open(".local_conf.yaml")) 
    except:
        print( 
            "Sobotka expected a .local_conf.yaml file to link this directory " \
            "to an existing project but did not find one. " \
            "Try sobotka up to create a new project instead") 


def store_local_conf(project_id):
    local_conf = {}
    local_conf["project_id"] = project_id
    with open('.local_conf.yaml', 'w') as yaml_file:
        yaml.dump(local_conf, yaml_file, default_flow_style=False)


def load_manifest():
    try:
        return yaml.safe_load(open("manifest.yaml")) 
    except:
        print( 
            "Sobotka expected a manifest.yaml file to define " \
            "the Project. Create this file in the root of your " \
            "project or cd to a dorectory where one exists to begin") 

##
## 
## CRUD PROJECTS
##
##

def create_project():

    config = load_manifest()

    ec2_manager = Ec2Manager()
    instance = ec2_manager.create_instance(
        ImageId=config["project"]["instance"]["image_id"], 
        KeyName=config["project"]["instance"]["key_name"], 
        SecurityGroupIds=config["project"]["instance"]["security_group_ids"],
        Name=config["project"]["shortname"]) 

    project = Project(
        shortname = config["project"]["shortname"],
        hostname = instance.public_dns_name,
        instance_id = instance.id,
        username = config["project"]["username"],
        key_file = config["project"]["key_file"],
        code_dir=config["project"]["code_dir"],
        docker_compose=config["project"]["docker_compose"],
        public_ip=instance.public_ip_address,
        created_at=utcnow())  
    project.set_host_string()

    project.save()
    store_local_conf(project.id)
    print("Successfully created project")
    print(project)


    ssh_conf = SshConfigFileManager()
    ssh_conf.add_host(
        name = config["project"]["shortname"], 
        user = config["project"]["username"], 
        hostname = instance.public_dns_name, 
        key_file = config["project"]["key_file"])


    hosts_file = HostsFileManager()
    hosts_file.add_entry(project.public_ip, project.shortname)

    return project


def print_info():
    project = get_project_from_local_conf()
    print(project)

def get_project_from_local_conf():
    local_conf = load_local_conf()
    project_id = local_conf["project_id"]
    project = Project.get(Project.id == project_id)
    return project

def destroy_project():
    project = get_project_from_local_conf()

    hosts_file = HostsFileManager()
    hosts_file.remove_entry(project.public_ip, project.shortname)

    ec2_manager = Ec2Manager()
    ec2_manager.terminate_instance(project.instance_id)

    ssh_conf = SshConfigFileManager()
    ssh_conf.remove_host(project.shortname)

    project.destroy()
    os.system("rm .local_conf.yaml")


##
## 
## REMOTE COMMAND RUNNER
##
##

def run():
    project = get_project_from_local_conf()
    runner = RemoteCommandRunner(project)
    runner.compose_up()

def stop():
    project = get_project_from_local_conf()
    runner = RemoteCommandRunner(project)
    runner.compose_stop()

def bootstrap():
    project = get_project_from_local_conf()
    runner = RemoteCommandRunner(project)
    runner.bootstrap_compose() 

def execute_command():
    command = args.command
    project = get_project_from_local_conf()
    runner = RemoteCommandRunner(project)
    runner.execute_arbitrary_command(command)   

def get_logs():
    project = get_project_from_local_conf() 
    runner = RemoteCommandRunner(project)
    runner.show_compose_logs()

##
## 
## FILE SYNC OPERATIONS
##
##

def push():
    project = get_project_from_local_conf()
    fsync = FileSyncUtility()
    fsync.push_directory(project)

def watch_directory():
    project = get_project_from_local_conf()
    fsync = FileSyncUtility()
    fsync.watch_directory(project)


##
## 
## CLI HELPER FUCTIONS
##
##

def has_sudo():
    if os.getuid() == 0:
        return True
    else:
        print("This operation requires elevated privelages, please try again with sudo")
        exit(126)   

def ssh():
    project = get_project_from_local_conf()
    project.connect()

def create_key_pair():
    kpm = KeyPairManager()
    kpm.create_key_pair()


def utcnow():
    # An ISO 8601 string represention of the current time _including_ timezone (UTC)
    return datetime.datetime.now(tz=pytz.utc).isoformat()

##
## 
## MAIN LOGIC 
##
##
db.create_tables(Project)

parser = argparse.ArgumentParser(description='Sobotka is kewl')
parser.add_argument('action', default=False, nargs='?')
parser.add_argument('command', default=None, nargs='?')
args = parser.parse_args()

if args.action == "init":
    if has_sudo():
        create_project()
elif args.action == "list":
    Project.list_all()
elif args.action == "info":
    print_info()
elif args.action == "ssh":
    ssh()
elif args.action == "exec":
    execute_command() 
elif args.action == "push":
    push()    
elif args.action == "bootstrap":
    bootstrap()  
elif args.action == "run":
    run()
elif args.action == "stop":
    stop()    
elif args.action == "destroy":
    if has_sudo():
        destroy_project()
elif args.action == "watch":
    watch_directory()    
elif args.action == "logs":
    get_logs()    
elif args.action == "key":
    create_key_pair()                           
else:
    print("Not doing anything")    
