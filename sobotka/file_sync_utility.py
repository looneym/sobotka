from subprocess import call
import os
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

class OnChangeHandler(FileSystemEventHandler):
    
    def __init__(self, observer, project):
        self.observer = observer
        self.project = project
        self.fsync = FileSyncUtility()

    def on_any_event(self, event):
        print("Something's changed! Syncing directory with remote host")
        self.fsync.push_directory(self.project)
        print("Done")

class FileSyncUtility():
           
    def push_directory(self, project):
        host = project.shortname
        remote_dir = project.code_dir
        os.system("rsync -r ./ {}:{}".format(host,remote_dir))

    def watch_directory(self, project): 
        host = project.shortname
        remote_dir = project.code_dir
        print("Watching for changes...")
        print("Any changes made to this directory will be pushed to the remote host automatically")
        path = '.'
        observer = PollingObserver()
        event_handler = OnChangeHandler(observer, project)

        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()




