from sys import exit
import argparse
import os 

import db
import helpers
import yaml_util
from models import Project 
from aws import Ec2Manager
from remote_command_runner import RemoteCommandRunner 
from file_sync_utility import FileSyncUtility
from hosts_file_manager import HostsFileManager
from ssh_config_file_manager import SshConfigFileManager

def create_key_pair(oveerride):
     helpers.create_key_pair(override)
                                
def create_project():

    config = yaml_util.load_manifest()

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
        created_at=helpers.utcnow())  
    project.set_host_string()

    project.save()
    yaml_util.store_local_conf(project.id)
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
    local_conf = yaml_util.load_local_conf()
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

def ssh():
    project = get_project_from_local_conf()
    project.connect()    


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

def execute_command(command):
    project = get_project_from_local_conf()
    runner = RemoteCommandRunner(project)
    runner.execute_arbitrary_command(command)   

def get_logs():
    project = get_project_from_local_conf() 
    runner = RemoteCommandRunner(project)
    runner.show_compose_logs()

def push():
    project = get_project_from_local_conf()
    fsync = FileSyncUtility()
    fsync.push_directory(project)

def watch_directory():
    project = get_project_from_local_conf()
    fsync = FileSyncUtility()
    fsync.watch_directory(project)

def main():

    db.create_tables(Project)

    description_string = (
        'Manage development environments on AWS: '
        'https://github.com/looneym/sobotka/blob/master/docs/usage.md'
        )
    parser = argparse.ArgumentParser(description=description_string)
    parser.add_argument('action')
    parser.add_argument('command', nargs='?')
    parser.add_argument("-o", "--overwrite", help="Overwrite existing key pair", action="store_true")
    args = parser.parse_args()

    if args.action == "init":
        if helpers.has_sudo():
            create_project()
    elif args.action == "list":
        Project.list_all()
    elif args.action == "info":
        print_info()
    elif args.action == "ssh":
        ssh()
    elif args.action == "exec":
        execute_command(args.command) 
    elif args.action == "push":
        push()    
    elif args.action == "bootstrap":
        bootstrap()  
    elif args.action == "run":
        run()
    elif args.action == "stop":
        stop()    
    elif args.action == "destroy":
        if helpers.has_sudo():
            destroy_project()
    elif args.action == "watch":
        watch_directory()    
    elif args.action == "logs":
        get_logs()    
    elif args.action == "key":
      helpers.create_key_pair(args.overwrite)
    else:
        print("Please specify an action")    

if __name__ == "__main__":
    main()
    
