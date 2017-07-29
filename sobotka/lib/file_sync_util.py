from subprocess import call
import os
import sys
import time
import logging

            
def sync_directory(host, remote_dir):
    os.system("rsync -r ./ {}:{}".format(host,remote_dir))


def watch_directory(host, remote_dir):
    print("Watching for changes...")
    print("Any changes made to this directory will be pushed to the remote host automatically")
    while True:
        os.system("rsync -r ./ {}:{}".format(host,remote_dir))
        time.sleep(1)

