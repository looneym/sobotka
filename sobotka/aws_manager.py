import boto3

class AwsManager:


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



    
