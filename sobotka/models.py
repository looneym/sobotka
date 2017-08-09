from os.path import expanduser
import os
from peewee import * 
from subprocess import call
import db as sobotka_db
 
class BaseModel(Model):
    class Meta:
        database = sobotka_db.get_database()


class Project(BaseModel):
    shortname = CharField()
    hostname = CharField()
    username = CharField()
    instance_id = CharField()
    ssh_string = CharField()
    host_string = CharField()
    key_file = CharField()
    code_dir = CharField()
    docker_compose = BooleanField()
    public_ip = CharField()
    created_at = CharField()

    def destroy(self):
        q = self.delete()
        q.execute() 

    def connect(self):
        call(["ssh", self.shortname])

    # TODO: add created at field
    def __repr__(self):
        return "[PROJECT] id: {}, " \
               "shortname: {}, " \
               "hostname: {}," \
               "public_ip: {}" \
               "created_at: {}".format(
                        self.id,
                        self.shortname,
                        self.hostname,
                        self.public_ip,
                        self.created_at)          
    @classmethod
    def get_all(cls):
        projects = []
        for project in cls.select():
            projects.append(project)
        return projects    

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
         