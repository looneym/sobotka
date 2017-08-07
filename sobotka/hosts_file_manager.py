from python_hosts import Hosts, HostsEntry

class HostsFileManager:

    def __init__(self):
        self.my_hosts = Hosts()

    def add_entry(self, ip, name):
        name = name + ".dev"
        # just to be safe
        self.remove_entry(ip, name)

        new_entry = HostsEntry(entry_type='ipv4', address=ip, names=[name])
        self.my_hosts.add([new_entry])
        self.my_hosts.write()

    def remove_entry(self, ip, name):
        name = name + ".dev"
        self.my_hosts.remove_all_matching(address=ip)
        self.my_hosts.remove_all_matching(name=name)
        self.my_hosts.write()


