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

def compose_rebuild(project):
    configure(project)
    with cd(project.code_dir):  
        run("sudo docker-compose stop")
        run("sudo docker-compose up --build")
    fabric.network.disconnect_all()     

def compose_logs(project):
    configure(project)
    try: 
        with cd(project.code_dir):  
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





