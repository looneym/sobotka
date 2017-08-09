This file describes how your project needs to be structured in order to work with Sobotka. You can refer to the [hello world example project repository](https://github.com/looneym/sobotka-example) in order to view the source code and configuration files for a functional project.

## The `docker-compose` file

Sobotka uses `docker-compose` to orchestrate multiple dependant services. `docker-compose` can be used to create complex distributed systems however the requirements for using Sobotka are relativly few:

- The directory containing your code must be mounted as a volume rather than being snapshotted in the container at creation time using `ADD` or `COPY`. This allows file changes on your local machine to be persisted first to the EC2 instance and then down into the container
- The ports used by your application need to be mapped to open ports as defined by your EC2 security group (see the aws_configuration.md file for more details on this)
- The command to start your application should be located in the `docker-compose` file rather than the Dockerfile for that particular service. 


## Live reload

Sobotka will handle persisting your code changes down to the container but your application will also need to detect these changes and reload itself automatically. In the example project, running the app with the `debug` flag set to `True` takes care of this for us. 


## The `manifest.yaml` file

This should be places in the root of your repository. See the `usage.md` documentation file for more information