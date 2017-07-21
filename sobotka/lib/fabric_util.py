## Right now this module file contains all the methods
## for remotely executing commands on the host

## This should be changed to multiple modules: one for 
## git, one for docker-compose, one for general file operations
## one for other build systems etc. 

## The goal of these modules is to work as plugins, providing
## a technology-specific implementation for behaviour
## exposed by the Project model's methods

from __future__ import with_statement
from fabric.contrib.console import confirm
from fabric.api import env, run, cd
import fabric

def configure(project):
    global env
    env.host_string = project.host_string
    env.key_filename = project.key_file
    env.output_prefix = False

def bootstrap_compose(project):
    configure(project)
    run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
    run("sudo add-apt-repository 'deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable'")
    run("sudo apt-get update")
    run("sudo apt-get install -y docker-ce docker-compose")
    run("sudo usermod -aG docker ${USER}")

def pull_repo(host_string, key_file, repo_url):
    env.host_string = host_string
    env.key_filename = key_file
    env.output_prefix = False
    run("git clone {}".format(repo_url))    

def compose_up(project):
    configure(project)
    with cd(project.code_dir):
        run("sudo docker-compose up -d")

def compose_stop(host_string, key_file, code_dir):
    env.host_string = host_string
    env.key_filename = key_file
    env.output_prefix = False
    with cd(code_dir):  
        run("sudo docker-compose stop")

def compose_logs(host_string, key_file, code_dir):
    env.host_string = host_string
    env.key_filename = key_file
    env.output_prefix = False
    try: 
        with cd(code_dir):  
            run("sudo docker-compose logs -f")
    except KeyboardInterrupt:
        # Custom interrupt handler to close connection
        # and stop log output from spamming the console
        fabric.network.disconnect_all()         

def remove_dir(host_string, key_file, code_dir):
    env.host_string = host_string
    env.key_filename = key_file
    env.output_prefix = False
    run("rm -rf {}".format(code_dir))        


def execute_arbitrary_command(project, command):
    configure(project)
    run(command)



