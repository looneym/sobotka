from storm.parsers.ssh_config_parser import ConfigParser as StormParser
from os.path import expanduser

def add_host(name, user, hostname, key_file):
    sconfig = StormParser(expanduser("~/.ssh/config"))
    sconfig.load()
    sconfig.add_host(name, {
        'user': user,
        'hostname': hostname,
        'IdentityFile': key_file
    })
    sconfig.write_to_ssh_config()


def remove_host(name):
    sconfig = StormParser(expanduser("~/.ssh/config"))
    sconfig.load()
    sconfig.delete_host(name)
    sconfig.write_to_ssh_config()
