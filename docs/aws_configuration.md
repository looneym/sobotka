This file details configuration requirements which are specific to AWS. You can refer to this example manifest file to see how the options dicussed are specified in practice:

```
project:
    shortname: sobotka-example
    code_dir: sobotka-example
    key_file: ~/.ssh/sobotka.pem
    username: ubuntu
    docker_compose: true  
    instance:
        image_id: ami-835b4efa
        key_name: sobotka
        security_group_ids:
            - sg-f4d6168e
```


## Credentials

There are two sets of credentials which much be configured in order to use Sobotka:

- An AWS access key (used to talk to the AWS API)
- An SSH key pair (used for SSH access to the remote hosts you create)

### AWS access key

Sobotka uses the boto3 library to communicate with AWS. This library has many ways of accepting user credentials, all of which are outlined in their official documentation [here](http://boto3.readthedocs.io/en/latest/guide/configuration.html)

The simplest way of getting this working howver is to simply create a config file in `~/.aws/config`. 

Below is an example of a minimal but perfectly functional configuration file using placeholder values for secrets: 

```
[default]
aws_access_key_id=foo
aws_secret_access_key=bar 
region=us-west-2
```

NOTE: Never share these key values publicly!

You will need to generate your own access key from the AWS web interface. The AWS documentation on how to do this is [here](http://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html)

You can specify whichever region you like but note that the security group you specify for you project in `manifest.yaml` will need to be valid for this region. Please see the security groups documentation below for more information.

These options are not specified in the project manifest, just read directly from the config file.

### SSH key pair

When creating an EC2 instance, we specify a key pair which will later be used to access the instance over SSH. You will need to have this key file stored on your local machine in order to proceed. 

Again, there are many options here but the simplest way to get up and runing is to use `sobotka key` to generate a key file via the API (having a correctly congigured aws config file is a prerequisite for this step0. This command will create a key named `sobotka` and store the file in `~/.ssh/sobotka.pem`. You can then use these defaults in your `manifest.yaml` file:


## AMI

An AMI (Amazon Machine Image) specifies what kind of EC2 instance you will be creating. There are many to choose from; you can refer to Amazon's [documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami.html) for further help. Sobotka requries an id value for an AMI in order to work. 

Note that the default username may be different depending on the AMI you choose. Sobotka requires the correct username value to be specified in the manifest in order to allow for SSH access. The example manifest file uses a basic Ubuntu 16 image with a corresponding `ubuntu` username

## Security Groups

The security group specifies the rules for inbound traffic to the host. If your application needs an open port such as port 80 for web traffic, you will need a security group which allows for this. 

You can create a new security group by logging in to the AWS web console, choosing EC2 from the services menu then navigating to Security Groups on the left hand side. 

The security group used in the examples has the following rules:

```
Type  Protocol Port Range Source
HTTP  TCP      80         0.0.0.0/0
HTTP  TCP      80         ::/0
SSH   TCP      22         0.0.0.0/0
```

These settigns allow for inbound web traffic and SSH traffic from ALL IPs: you may wish to implement more restrictive rules for additional securiity.

Amazon's documenation is [here](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-network-security.html)
