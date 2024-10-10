#!/usr/bin/env python3

import socket, sys, os, time

from watchdog.events import DirCreatedEvent, DirDeletedEvent, DirModifiedEvent, DirMovedEvent, FileClosedEvent, FileCreatedEvent, FileDeletedEvent, FileModifiedEvent, FileMovedEvent, FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

FILES_PATH = "testing"

class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        print("on_any_event: {}".format(event))
    
    def on_closed(self, event: FileClosedEvent) -> None:
        print("on_closed: {}".format(event))   
    
    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        print("on_created: {}".format(event))  
    
    def on_deleted(self, event: DirDeletedEvent | FileDeletedEvent) -> None:
        print("on_deleted: {}".format(event))  

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        print("on_modified: {}".format(event)) 

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        print("on_moved: {}".format(event))    


if __name__ == "__main__":
    event_handler = EventHandler() 
    observer = Observer()
    observer.schedule(event_handler, FILES_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()