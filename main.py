import boto3
from IPython import embed
import os
from peewee import *

db = SqliteDatabase('sobotka.db')

class Host(Model):
    shortname = CharField()
    hostname = CharField()
    username = CharField()
    instance_id = CharField()
    ssh_string = CharField()

    def get_instance(self):
    	return ec2.Instance(self.instance_id)

    def connect(self):
       os.system(self.ssh_string)     

    class Meta:
        database = db # Th


db.connect()

try:
    db.create_tables([Host])  
except peewee.OperationalError:
	continue

ubuntu = "ami-835b4efa"
key_name = "boto_test"

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
		ssh_string = get_ssh_string(instance)
		)
	host.save

	return host

	

def get_ssh_string(instance):
	hostname = instance.public_dns_name
	# todo: fetch from config
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




host = create_host()

embed()



