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

    def set_host_string(self):
            host_string = self.username
            host_string += "@"
            host_string += self.hostname
            self.host_string = host_string         
    
    @classmethod
    def get_all(cls):
        projects = []
        for project in cls.select():
            projects.append(project)
        return projects   

    def __repr__(self):
        return "[PROJECT] id: {}, " \
               "shortname: {}, " \
               "hostname: {}, " \
               "public_ip: {}, " \
               "created_at: {}".format(
                        self.id,
                        self.shortname,
                        self.hostname,
                        self.public_ip,
                        self.created_at) 