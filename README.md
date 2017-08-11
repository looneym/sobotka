# Sobotka

### Description 

Sobotka is a command line tool for managing containerized remote development environments on AWS' EC2.

Features

- Provisioning EC2 instances
- Syncing files in your local directory with the remote host; facilitates live application reload
- Botstrapping the host with `docker` and `docker-compose`
- Running the application with `docker-compose up`

Using Sobotka involves defining and working with Projects. A Project is an object which represents a cloud-based 
development environment, including a remote host, dependancies and project code. 

A Project is first defnied in a` manifest.yml` file in the root of your project directory.

After running the `init` command, a project is created and associated with the current local directory. Further operations are performed with short command line instructions. 


***

### Quick start

1. Install Sobotka:

`pip install sobotka`

2. Clone the example app repository:

`git clone https://github.com/looneym/sobotka-example.git`

`cd sobotka-example`

3. Generate a SSH key with: 

`sobotka key`

Optionally use an existing key pair, updating the manifest as required. 

4. Create a config file in `~/.aws/config` with AWS API access key and region. You'll also need to set up a security group. See the [aws configuration docs](https://github.com/looneym/sobotka/blob/master/docs/aws_configuration.md) for more info

5. Run the following commands in the project directory:

```
sobotka init
sobotka bootstrap
sobotka push
sobotka run
```

5. Navigate to http://sobotka-example.dev in your browser to access your application! 


****

More detailed usage instructions can be found [here](https://github.com/looneym/sobotka/blob/master/docs/usage.md)


### Documentation Index

[Documentation is available here](https://github.com/looneym/sobotka/blob/master/docs/)


### Configuration / Requirements

- **AWS:** API access credentials as well as an SSH key pair. You also need to define a security group on AWS which specifies the rules for inbound traffic to the host. More details in the documentation on [AWS configuration requirements](https://github.com/looneym/sobotka/blob/master/docs/aws_configuration.md)
- **Your own applicaton:** Your application itself must be dockerized and comprize of one or more services (e.g. web, redis, DB) defined in a `docker-compose.yml` file which also specifies any network rules and volumes required for the application. Application requirements are discussed in more detail [here.](https://github.com/looneym/sobotka/blob/master/docs/aws_configuration.md)
 
### Use case

Sobotka solves a similar problem as Vagrant: define your environment along with your project code to eliminate differences between indvidual developers, prevent conflicts and dependency issues on your local machine, easily share example code and projects between people and keep a versioned history of your environment. Since Sobotka uses `docker-compose` it's easy to move your dev code into production environment configured using the same technology. 

Since Sobotka requires no VM on the local machine and minimal configuration it's an easy way to get a new machine up and running as a dev box as well as allowing you to offload the computational cost to the cloud to facilitate development on underpowered machines

### Something broken?

Please open an [issue](https://github.com/looneym/sobotka/issues)

