import os
from peewee import * 
from subprocess import call

class Project(Model):
    shortname = CharField()
    hostname = CharField()
    username = CharField()
    instance_id = CharField()
    ssh_string = CharField()
    host_string = CharField()
    key_file = CharField()
    code_dir = CharField()
    docker_compose = BooleanField()
    ip = CharField()

    def destroy(self):
        q = self.delete()
        q.execute() 

    def connect(self):
        call(["ssh", self.shortname])

    # TODO: add created at field
    def __repr__(self):
        return "[PROJECT] id: {}, " \
               "shortname: {}, " \
               "hostname: {} ".format(
                        self.id,
                        self.shortname,
                        self.hostname)          
    @classmethod
    def list_all(cls):
        projects = []
        for project in cls.select():
            print project

##
## 
## EVERYTHING BELOW THIS IS A HORRIBLE HACK
##
##
  
    def set_ssh_string(self, instance, key_file):
        hostname = instance.public_dns_name
        username = "ubuntu"
        ssh_string = "ssh"
        ssh_string += " "
        ssh_string += "-i"
        ssh_string += " "
        ssh_string += key_file
        # ssh_string += "~/.ssh/"
        # ssh_string += key_name
        # ssh_string += ".pem"
        ssh_string += " "
        ssh_string += username
        ssh_string += "@"
        ssh_string += hostname
        self.ssh_string = ssh_string

    def set_host_string(self, instance):
            hostname = instance.public_dns_name
            username = "ubuntu"
            host_string = username
            host_string += "@"
            host_string += hostname
            self.host_string = host_string         
         
db = SqliteDatabase('sobotka.db')
db.connect()
try:
    db.create_tables([Project])  
except OperationalError:
    pass
