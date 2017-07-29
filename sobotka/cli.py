import models
from lib import aws_util, fabric_util, helpers, file_sync_util, ssh_config_util
from IPython import embed
import yaml
import argparse

Project = models.Project

parser = argparse.ArgumentParser(description='Sobotka is kewl')
parser.add_argument('action', default=False, nargs='?')
parser.add_argument('command', default=None, nargs='?')

def sync():
    project = get_project_from_local_conf()

    file_sync_util.sync_directory(
        host = project.shortname,
        remote_dir = project.code_dir
        )

def get_project_from_local_conf():
    local_conf = load_local_conf()
    project_id = local_conf["project_id"]
    project = Project.get(Project.id == project_id)
    return project


def store_local_conf(project_id):
    local_conf = {}
    local_conf["project_id"] = project_id
    with open('.local_conf.yaml', 'w') as yaml_file:
        yaml.dump(local_conf, yaml_file, default_flow_style=False)

def ssh():
    project = get_project_from_local_conf()
    project.connect()

def load_local_conf():
    try:
        return yaml.safe_load(open(".local_conf.yaml")) 
    except:
        print( 
            "Sobotka expected a .local_conf.yaml file to link this directory " \
            "to an existing project but did not find one. " \
            "Try sobotka up to create a new project instead") 

def load_manifest():
    try:
        return yaml.safe_load(open("manifest.yaml")) 
    except:
        print( 
            "Sobotka expected a manifest.yaml file to define " \
            "the Project. Create this file in the root of your " \
            "project or cd to a dorectory where one exists to begin") 

def create_project():

    config = load_manifest()

    instance = aws_util.create_instance(
        ImageId=config["project"]["instance"]["image_id"], 
        KeyName=config["project"]["instance"]["key_name"], 
        SecurityGroupIds=config["project"]["instance"]["security_group_ids"],
        Name=config["project"]["shortname"]) 

    project = Project(
        shortname = config["project"]["shortname"],
        hostname = instance.public_dns_name,
        instance_id = instance.id,
        username = config["project"]["username"],
        ssh_string = helpers.get_ssh_string(instance, config["project"]["key_file"]),
        host_string = helpers.get_host_string(instance),
        key_file = config["project"]["key_file"],
        repo_url = config["project"]["repo_url"],   
        code_dir=config["project"]["code_dir"],
        docker_compose=config["project"]["docker_compose"])

    project.save()
    store_local_conf(project.id)
    print("Successfully created project")
    print(project)

    ssh_config_util.add_host(
        name = config["project"]["shortname"], 
        user = config["project"]["username"], 
        hostname = instance.public_dns_name, 
        key_file = config["project"]["key_file"])

    return project


def run():
    project = get_project_from_local_conf()
    fabric_util.compose_up(project)

def bootstrap():
    project = get_project_from_local_conf()
    fabric_util.bootstrap_compose(project)     

def print_info():
    project = get_project_from_local_conf()
    print(project)

def execute_command():
    command = args.command
    project = get_project_from_local_conf()
    fabric_util.execute_arbitrary_command(project, command)    


def destroy_project()
    project = get_project_from_local_conf()
    project.destroy()

def watch_directory()
    pass

args = parser.parse_args()
print(args)

if args.action == "init":
    create_project()
elif args.action == "list":
    Project.list_all()
elif args.action == "info":
    print_info()
elif args.action == "ssh":
    ssh()
elif args.action == "exec":
    execute_command() 
elif args.action == "sync":
    sync()    
elif args.action == "bootstrap":
    bootstrap()  
elif args.action == "run":
    run()
elif args.action == "destroy":
    destroy_project()
elif args.action == "watch":
    watch_directory()                     
else:
    print("Not doing anything")    

    
