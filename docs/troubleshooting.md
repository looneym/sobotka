Documenting the fixes to some issues I've run into so far. 

### Can't connect via ssh
If your ssh client cannot resolve the shortname for a host but there is a corresponding entry in your '~/.ssh/config' file there is likely an issue with the permissions of this file which is causing ssh to read from the system-wide config file in 'etc' instead. 

Running the following commands in your home directory should help:

'''
sudo chmod 600 ~/.ssh/*
sudo chmod 644 ~/.ssh/config
'''
