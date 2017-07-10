import boto3

ec2 = boto3.resource('ec2')

def create_instance(ImageId, KeyName, SecurityGroupIds):
    print("Creating EC2 instance on AWS. This can take some time")
    instances = ec2.create_instances(
        ImageId=ImageId,
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName=KeyName,
        SecurityGroupIds=SecurityGroupIds)
    instance = instances[0]
    instance.wait_until_running()
    instance.load()
    return instance

def find_instance(instance_id):
    return ec2.Instance(instance_id)

    
