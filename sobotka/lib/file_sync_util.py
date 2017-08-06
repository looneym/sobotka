from subprocess import call
import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileModifiedEvent
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

import fabric_util

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer, project):
        self.observer = observer
        self.project = project

    def on_any_event(self, event):
        print("Something's changed! Syncing directory with remote host")
        push_directory(self.project)
        if self.project.docker_compose:
            print("Rebuilding containers on remote host")
            fabric_util.compose_rebuild(self.project)
        print("Done")
           
def push_directory(project):
    host = project.shortname
    remote_dir = project.code_dir
    os.system("rsync -r ./ {}:{}".format(host,remote_dir))

def watch_directory(project): 
    host = project.shortname
    remote_dir = project.code_dir
    print("Watching for changes...")
    print("Any changes made to this directory will be pushed to the remote host automatically")
    path = '.'
    observer = PollingObserver()
    event_handler = MyEventHandler(observer, project)

    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()




