from __future__ import with_statement
from fabric.contrib.console import confirm
from fabric.api import env, run, cd
import fabric

class RemoteCommandRunner:

    def __init__(self, project):
        self.project = project

        global env
        env.host_string = project.host_string
        env.key_filename = project.key_file
        env.output_prefix = False

    def bootstrap_compose(self):
        run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
        run("sudo add-apt-repository 'deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable'")
        run("sudo apt-get update")
        run("sudo apt-get install -y docker-ce docker-compose")
        run("sudo usermod -aG docker ${USER}")  

    def compose_up(self):
        with cd(self.project.code_dir):
            run("sudo docker-compose up -d")

    def compose_stop(self):
        with cd(self.project.code_dir):  
            run("sudo docker-compose stop")

    def compose_rebuild(project):
        configure(project)
        with cd(project.code_dir):  
            run("sudo docker-compose stop")
            run("sudo docker-compose up --build")
        fabric.network.disconnect_all()     

    def show_compose_logs(self):
        try: 
            with cd(self.project.code_dir):  
                run("sudo docker-compose logs -f")
        except KeyboardInterrupt:
            # Custom interrupt handler to close connection
            # and stop log output from spamming the console
            fabric.network.disconnect_all()            

    def execute_arbitrary_command(self, command):
        run(command)





