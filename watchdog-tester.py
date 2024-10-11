#!/usr/bin/env python3

import socket, sys, os, time

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

FILES_PATH = "testing"

class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        print("Class '{}', SrcPath '{}', DestPath '{}', EventType '{}', IsDirectory '{}', IsSynthetic '{}'".format(
            event.__class__.__name__, event.src_path, event.dest_path, event.event_type, event.is_directory, event.is_directory
        ))


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