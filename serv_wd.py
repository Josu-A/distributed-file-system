#!/usr/bin/env python3

import socket, sys, os, time
import szasar

from watchdog.events import DirCreatedEvent, DirDeletedEvent, DirModifiedEvent, DirMovedEvent, FileCreatedEvent, FileDeletedEvent, FileModifiedEvent, FileMovedEvent, FileSystemEventHandler
from watchdog.observers import Observer

PORT = szasar.WATCHDOG_PORT
FILES_PATH = szasar.CLIENT_FILES_PATH


class EventHandler(FileSystemEventHandler):
    def __init__(self, dialog: socket.socket):
        self.dialog = dialog

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        if isinstance(event, FileModifiedEvent):
            file_path = event.src_path
            file_size = os.path.getsize(file_path)
            if os.path.exists(file_path):
                message = f"FIMD{file_path}?{file_size}\r\n"
                self.dialog.sendall(message.encode("ascii"))

    def on_deleted(self, event: DirDeletedEvent | FileDeletedEvent) -> None:
        if isinstance(event, FileDeletedEvent):
            file_path = event.src_path
            message = f"FIDL{file_path}\r\n"
            self.dialog.sendall(message.encode("ascii"))
        elif isinstance(event, DirDeletedEvent):
            dir_path = event.src_path
            message = f"DIDL{dir_path}\r\n"
            self.dialog.sendall(message.encode("ascii"))

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        if isinstance(event, FileMovedEvent):
            file_path_src = event.src_path
            file_path_dest = event.dest_path
            if os.path.exists(file_path_dest):
                message = f"FIMV{file_path_src}?{file_path_dest}\r\n"
                self.dialog.sendall(message.encode("ascii"))

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        if isinstance(event, DirCreatedEvent):
            dir_path = event.src_path
            message = f"DICR{dir_path}\r\n"
            self.dialog.sendall(message.encode("ascii"))


def session(s: socket.socket) -> None:
    event_handler = EventHandler(s)
    observer = Observer()
    observer.schedule(event_handler, FILES_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('', PORT))
    s.listen(5)

    while True:
        dialog, address = s.accept()
        print("Conexión accepted from socket {0[0]}:{0[1]}.".format(address))
        s.close()
        session(dialog)
        dialog.close()
        exit(0)