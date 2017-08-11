from storm.parsers.ssh_config_parser import ConfigParser as StormParser
from os.path import expanduser

class SshConfigFileManager:

    def add_host(self, name, user, hostname, key_file):
        sconfig = StormParser(expanduser("~/.ssh/config"))
        sconfig.load()

        # Remove existig hosts with that name to avoid dupes
        try:
            sconfig.delete_host(name)
        except ValueError:
            # Host not found
            pass    
        sconfig.add_host(name, {
            'user': user,
            'hostname': hostname,
            'IdentityFile': key_file,
            "StrictHostKeyChecking": "no"
        })
        sconfig.write_to_ssh_config()


    def remove_host(self, name):
        sconfig = StormParser(expanduser("~/.ssh/config"))
        sconfig.load()
        sconfig.delete_host(name)
        sconfig.write_to_ssh_config()
