import os
from peewee import * 
from subprocess import call

from lib import aws_util, fabric_util, ssh_config_util

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

    # return an instance object representing the EC2 host the project is running on 
    def get_instance(self):
        return aws_util.find_instance(self.instance_id)

    # Nuke the whole thing
    def destroy(self):
        aws_util.find_instance(self.instance_id).terminate()  
        ssh_config_util.remove_host(self.shortname)
        q = self.delete()
        q.execute() 

    # open interactive ssh session
    def connect(self):
        call(["ssh", self.shortname])

    # returns a dictionary representing the attributes of the object
    def attributes(self):
        return self.__dict__["_data"]    

    # returns a list representing names of the object's attributes
    def attribute_names(self):
        return self.__dict__["_data"].keys()   

    # Human-readable description of the project
    # TODO: add created at field
    def __repr__(self):
        return "[PROJECT] id: {}, " \
               "shortname: {}, " \
               "hostname: {} ".format(
                        self.id,
                        self.shortname,
                        self.hostname)          

    # Generic high level methods for various tasks useful for interacting
    # with your project environment
    # currenly only support is for docker-compose but could be expanded
    # to allow for alternative build tools via more fabric plugins 
    def bootstrap(self):
        if self.docker_compose:
            fabric_util.bootstrap_compose(
                self.host_string, 
                self.key_file)   
   
    def up(self):
        if self.docker_compose:
            fabric_util.compose_up( 
                self.host_string, 
                self.key_file, 
                self.code_dir)

    def stop(self):
        if self.docker_compose:
            fabric_util.compose_stop(
                    self.host_string, 
                    self.key_file,
                    self.code_dir)   

    def logs(self):
        if self.docker_compose:
            fabric_util.compose_logs(
                    self.host_string, 
                    self.key_file,
                    self.code_dir)

    @classmethod
    def list_all(cls):
        projects = []
        for project in cls.select():
            print project

             
## Gonna need a better way of managing the DB
## Probably store in in the user's app data folder or something
db = SqliteDatabase('sobotka.db')
db.connect()
try:
    db.create_tables([Project])  
except OperationalError:
    pass
