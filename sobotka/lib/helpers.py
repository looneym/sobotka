# Need a better way to do this

def get_ssh_string(instance, key_file):
    hostname = instance.public_dns_name
    username = "ubuntu"

    ssh_string = "ssh"
    ssh_string += " "
    ssh_string += "-i"
    ssh_string += " "
    ssh_string += key_file
    # ssh_string += "~/.ssh/"
    # ssh_string += key_name
    # ssh_string += ".pem"
    ssh_string += " "
    ssh_string += username
    ssh_string += "@"
    ssh_string += hostname

    return ssh_string

def get_host_string(instance):
    hostname = instance.public_dns_name
    username = "ubuntu"
    host_string = username
    host_string += "@"
    host_string += hostname   

    return host_string 