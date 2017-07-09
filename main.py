from __future__ import with_statement
import boto3
from IPython import embed
import os
from peewee import *
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.api import env, run

db = SqliteDatabase('sobotka.db')

class Host(Model):
    shortname = CharField()
    hostname = CharField()
    username = CharField()
    instance_id = CharField()
    ssh_string = CharField()
    host_string = CharField()
    repo = CharField()

    def get_instance(self):
        return ec2.Instance(self.instance_id)

    def connect(self):
       os.system(self.ssh_string)

    def build_env(self):
        env.host_string = self.host_string
        env.key_filename = "~/.ssh/boto_test.pem"
        code_dir = 'docker-compose-hello-world'
        run("git clone https://github.com/looneym/docker-compose-hello-world.git")
        with cd(code_dir):
            run("sudo docker-compose up")


    def provision(self):
        env.host_string = self.host_string
        env.key_filename = "~/.ssh/boto_test.pem"
        run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
        run("sudo add-apt-repository 'deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable'")
        run("sudo apt-get update")
        run("sudo apt-get install -y docker-ce docker-compose")
     


db.connect()

try:
    db.create_tables([Host])  
except OperationalError:
    pass

ubuntu = "ami-835b4efa"
key_name = "boto_test"
repo = "https://github.com/joaojeronimo/docker-compose-hello-world.git"

ec2 = boto3.resource('ec2')

def create_host():
    instances = ec2.create_instances(
        ImageId=ubuntu,
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName=key_name,
        SecurityGroupIds=[
            'sg-f4d6168e',
        ]
    )
    instance = instances[0]
    instance.wait_until_running()
    instance.load()

    host = Host(
        shortname = "my_app",
        hostname = instance.public_dns_name,
        username = "ubuntu",
        instance_id = instance.id,
        ssh_string = get_ssh_string(instance),
        host_string = get_host_string(instance),
        repo = repo
        )
    host.save

    return host

    
# Need a better way to do this

def get_ssh_string(instance):
    hostname = instance.public_dns_name
    username = "ubuntu"

    ssh_string = "ssh"
    ssh_string += " "
    ssh_string += "-i"
    ssh_string += " "
    ssh_string += "~/.ssh/"
    ssh_string += key_name
    ssh_string += ".pem"
    ssh_string += " "
    ssh_string += username
    ssh_string += "@"
    ssh_string += hostname

    return ssh_string

def get_host_string(instance):
    hostname = instance.public_dns_name
    username = "ubuntu"
    host_string = username
    host_string += "@"
    host_string += hostname   

    return host_string 




host = create_host()

embed()



