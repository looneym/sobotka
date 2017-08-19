from os.path import expanduser
import os

import boto3

class Ec2Manager:

    def __init__(self):
        self.ec2 = boto3.resource('ec2')

    def create_instance(self, ImageId, KeyName, SecurityGroupIds, Name):
        print("Creating EC2 instance on AWS. This can take some time")
        instances = self.ec2.create_instances(
            ImageId=ImageId,
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            KeyName=KeyName,
            SecurityGroupIds=SecurityGroupIds)
        instance = instances[0]
        instance.wait_until_running()
        instance.load()

        self.ec2.create_tags(Resources=[instance.id], Tags=[{'Key':'name', 'Value': Name}])

        return instance

    def get_instance(self, instance_id):
        return self.ec2.Instance(instance_id)    

    def terminate_instance(self, instance_id):
        instance = self.get_instance(instance_id)  
        instance.terminate()  
  
class KeyPairManager:

    def __init__(self):
        self.KEY_PATH = '~/.ssh/sobotka.pem'
        self.KEY_NAME = 'sobotka'

    def create_key_pair(self, overwrite):
        if overwrite:
            self.delete_key_pair()
            
        ec2 = boto3.client('ec2')
        response = ec2.create_key_pair(KeyName=self.KEY_NAME)
        key_material = response['KeyMaterial']
        
        path = expanduser(self.KEY_PATH)
        key_file = open(path, 'w') 
        key_file.write(key_material) 
        key_file.close() 
        os.chmod(path, 0600)
        print('Created a new SSH key pair called {} and saved to {}'.format(self.KEY_NAME, self.KEY_PATH))

    def delete_key_pair(self):
        ec2 = boto3.client('ec2')
        ec2.delete_key_pair(KeyName='sobotka')    
   