import boto3

ec2 = boto3.resource('ec2')

def create_instance(ImageId, KeyName, SecurityGroupIds, Name):
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

    ec2.create_tags(Resources=[instance.id], Tags=[{'Key':'name', 'Value': Name}])

    return instance

def find_instance(instance_id):
    return ec2.Instance(instance_id)


# returns an array of all instances
def get_instances():
    instances_array = []
    instances = ec2.instances.all()
    for instance in instances:
        instances_array.append(instance)
    return instances_array   

# prints a human readable list of all instances
def list_instances():
    for instance in get_instances():
        print_readable_instance(instance)


def print_readable_instance(instance):
    name = "unnamed"
    if instance.tags is not None:
        for tag in instance.tags:
            if tag['Key'] == 'name':
                name = tag['Value']

    str = "[INSTANCE] id: {}, " \
          "state: {}, " \
          "name: {}, " \
          "public_dns_name: {} ".format(
                        instance.id,
                        instance.state["Name"],
                        name,
                        instance.public_dns_name)

    print str




    
