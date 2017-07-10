## Main application entry point, should define functions for various useful operations
## to be used in the interactive console
import models
from lib import aws_util, fabric_util, helpers
from IPython import embed
import yaml

Project = models.Project

def create_project():

    config = load_config()

    instance = aws_util.create_instance(
        ImageId=config["project"]["instance"]["image_id"], 
        KeyName=config["project"]["instance"]["key_name"], 
        SecurityGroupIds=config["project"]["instance"]["security_group_ids"]) 

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
    return project

def get_projects():
    return Project.select()  

def list_projects():
    for project in Project.select():
        print project

def load_config():
    try:
        return yaml.safe_load(open("manifest.yaml")) 
    except:
        print( 
            "Sobotka expected a manifest.yaml file to define " \
            "the Project. Create this file in the root of your " \
            "project or cd to a dorectory where one exists to begin") 


embed()



