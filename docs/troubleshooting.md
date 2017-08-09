Documenting the fixes to some issues I've run into so far. 

### Can't connect via ssh: unable to find host

If your ssh client cannot resolve the shortname for a host but there is a corresponding entry in your '~/.ssh/config' file there is likely an issue with the permissions of this file which is causing ssh to read from the system-wide config file in 'etc' instead. 

Running the following commands in your home directory should help:

```
sudo chmod 600 ~/.ssh/*
sudo chmod 644 ~/.ssh/config
```

### SSH permissions are too open error

If you've downloaded a key pair from the aws console, it may not have the correct permssions for use as acces to the file must be restricted to your own user account

This is easily fixed with `chmod 600 path_to_key_file`

You can also use `sobotka key` to generate a default key file insted which will automatically set the correct permissions for you. 
