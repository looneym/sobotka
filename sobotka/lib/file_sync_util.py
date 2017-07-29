from subprocess import call
import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer, host, remote_dir):
        self.observer = observer
        self.host = host
        self.remote_dir = remote_dir

    def on_any_event(self, event):
        print("Something's changed! Syncing directory with remote host")
        sync_directory(self.host, self.remote_dir)
        print("Done")

            
def sync_directory(host, remote_dir):
    os.system("rsync -r ./ {}:{}".format(host,remote_dir))

def watch_directory(host, remote_dir): 
    print("Watching for changes...")
    print("Any changes made to this directory will be pushed to the remote host automatically")
    path = '.'
    observer = Observer()
    event_handler = MyEventHandler(observer, host, remote_dir)

    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
