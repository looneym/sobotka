This file describes the process of using Sobotka. You can use the [hello world example project repository](https://github.com/looneym/sobotka-example) to follow along and get a feel for how it works.

### Setup and initial run

Ensure your AWS credentials are correct. See the aws_configuration.md documentation file for more details.


Define your `manifest.yaml`:

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

Refer to the project_configuration.md docs for anything not related to AWS

`cd` to the root directory of your project and run

`sobotka init`

This command:

- Provisions an EC2 instance 
- Adds an entry in your local `~/.ssh/config` file which aliases the newly created instance to the project shortname
- Adds an entry in the `/etc/hosts` file which maps the IP address of the instance to a URL comprising the project shortname with the `.dev` TLD e.g. `sobotka-example.dev`
- Creates a hidden file called 1local_conf.yaml`in your local directory to indicate a Sobotka project exists here. This file contains only the project_id which Sobotka will use to load the prject from it's own DB. You may wish to add this file to your `gitignore`.

Once the instance has spun up you can open an interactive SSH session quickly and easily by running

`sobotka ssh`

Note that even though Sobotka waits until the instance has finished loading completly before finishing the `init` commmand, it can still take a couple of seconds for the instance to accept SSH connections so you may need to wait a second or two

You can return to your local shell by executing the `exit` command or pressing ctrl+d

Push your project's code to the host with

`sobotka push`

 Bootstrap the host with docker and docker-compose with

`sobotka bootstrap`

Run your appliction:

`sobotka run`

If all goes well you can now open your browser and access the application at the shortname + `.dev` URL

http://sobotka-example.dev

To view the log output from your application call

`sobotka logs`

which will output a live tail of the `docker-compose` logs in your local terminal. Ctrl+c to exit.  

### Adding new features

Now it's time to get to work on developing your project. To use Sobotka, you make your changes locally and when you hit save, your changes will be pushed to your application. To make Sobotka watch your project for changes call

`sobotka watch`

If you're using the example project you can add a controller to see this in action. Paste this code into `server.py`:

```python
@app.route('/sobotka')
def sobotka():
    return "You're using Sobotka!"  
```
Then hit save. You'll see the `sobotka watch` terminal pane pick up the changes and the `sobotka logs` terminal pane indicate that the Flask app is retarting. 

Now visit http://sobotka-example.dev/sobotka in your browser to see your new route in action.

You should use your local terminal to commit changes to source control.

You can stop your application with `sobotka stop` when you're done.


### Deleting projects

Execute `sobotka destroy` to delete a project. This will:

- Terminate the EC2 instance
- Remove the entry in the hosts file and ssh config file
- Remove the `local_conf` file

You should view instances of projects as being quite ephemeral; you can spin them up and tear them down at any time. 

### Additional features

You can execute arbitrary commands on the remote host with 

`sobotka exec [command]`

e.g. `sobotka exec ls` or `sobotka exec apt-get install vim`

For interactive usage (such as opening an editor) you should use `sobotka ssh` to connect to the host instead. 

There are also some utility commands:

- Show all projects on your local machine with `sobotka list`
- Display info about the project in the current directory with `sobotka info`
- Create a new key file for use with EC2 using `sobotka key`