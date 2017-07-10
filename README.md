# Sobotka

![alt text](http://cdn.collider.com/wp-content/uploads/the-wire-season-2-tv-show-image-frank-sobotka.jpg)


### Description 

Capistrano-inspired configuration tool for creating containerized development environments on AWS. Named in honor of Frank Sobotka
from The Wire. 

Sobotka handles:

- Provisioning EC2 instances
- Botstrapping the host with `docker` and `docker-compose`
- Cloning your project from Github
- Running the environment with `docker-compose up`

These commands can all be carried out from an interactive console on your local machine. 

***

### Usage 

Using Sobotka involves defining and working with Projects. A Project is an object which represents a cloud-based 
development environment, including a remote host, dependancies and project code. 

#### 1. Define a project 

A Project is first defnied in a` manifest.yml` which shouldl live in the root of your project directory.

Example manifest file:

```
project:
    shortname: my_app
    repo_url: https://github.com/looneym/docker-compose-hello-world.git
    code_dir: docker-compose-hello-world
    key_file: ~/.ssh/boto_test.pem
    username: ubuntu
    docker_compose: true  
    instance:
        image_id: ami-835b4efa
        key_name: boto_test
        security_group_ids:
            - sg-f4d6168e
```

*Project Requirements:* Your application itself must be dockerized and comprize of one or more services (e.g. web, redis, DB)
defined in a `docker-compose.yml` file which also specifies any network rules and volumes required for the application. To find
out more on how to do this, read the official docs on docker-compose

#### 2. Boot the console

Running `python main.py` will drop you into an IPython interactive terminal with several useful functions loaded into context e.g.

- `create_project()` which will create a new project from a `manifest.xml` file in the current directory (you can navigate with `ls`
and `cd` as in a normal shell to move to any location where a manifest file exists)
- `list_projects()` prints a human readable list of current projects you have created
- `get_projects()` returns an iterable 

#### 3. Creating and working with projects

Create a new project with `project = create_project()` 

At this stage it has an empty EC2 instance which you can ssh into directly with `project.connect()` however the 
Project object provides multiple usful methods for provisioning your environment remotely:

- `project.bootstrap()` will install `docker` and `docker-compose`
- `project.pull_repo()` will pull the projects repo from a remote URL 
- `project.up()` calls `docker-compose up` in the project directory to launch your application
- `project.logs()` will call `docker-compose logs -f` to provide a live tail of the applications logs. Ctrl c to stop. 

***

### Installation and configuration

Clone the repo and install dependancies with pip. You will also need to configure the AWS command line client with securty credentials
Detailed instructions on this to be added later but following the boto3 tutorials should help for now. 

***

### Todo

Sobotka is still in very early development. The following features are planned:

- File sync over scp so that users can edit files locally and immediatly have changes pushed to the remote host
- Correctly configure local storage for the program
- Make available as a package via pip
- AWS module enhancements - list all instances, delete instances directly etc.
- General console improvements such as help menus and a better prompt
- Support for non-interacitve use in scripts









