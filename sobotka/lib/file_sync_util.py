from subprocess import call
import os

def sync_directory(host, remote_dir):
    os.system("rsync -r ./ {}:{}".format(host,remote_dir))
     