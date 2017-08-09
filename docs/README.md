Documentation for Sobotka

### Index

- [AWS configuration docs](https://github.com/looneym/sobotka/blob/master/docs/aws_configuration.md)
- [Project configuration docs](https://github.com/looneym/sobotka/blob/master/docs/project_configuration.md)
- [Detailed usage documentation](https://github.com/looneym/sobotka/blob/master/docs/usage.md)
- [Troubleshooting help](https://github.com/looneym/sobotka/blob/master/docs/troubleshooting.md)

### Quick start

1. Install Sobotka:

`pip install sobotka`

2. Clone the example app repository:

`git clone https://github.com/looneym/sobotka-example.git`

`cd sobotka-example`

3. Generate a SSH key with 

`sobotka key`

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


### Something broken?

Please open an [issue](https://github.com/looneym/sobotka/issues)