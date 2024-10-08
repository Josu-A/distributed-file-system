#!/usr/bin/env python3

import socket, sys, os, time
import szasar

from watchdog.events import DirCreatedEvent, DirDeletedEvent, DirModifiedEvent, DirMovedEvent, FileClosedEvent, FileCreatedEvent, FileDeletedEvent, FileModifiedEvent, FileMovedEvent, FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

PORT = 6013
FILES_PATH = "."


class State:
	Main, Uploading = range(2)


def sendOK( s, params="" ):
	s.sendall( ("OK{}\r\n".format( params )).encode( "ascii" ) )


def sendER( s, code=1 ):
	s.sendall( ("ER{}\r\n".format( code )).encode( "ascii" ) )


class EventHandler(FileSystemEventHandler):

    def __init__(self, dialog: socket.socket):
        self.dialog = dialog

    def on_any_event(self, event: FileSystemEvent) -> None:
        print(event)
    
    def on_closed(self, event: FileClosedEvent) -> None:
        print(event)
    
    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        print(event)
    
    def on_deleted(self, event: DirDeletedEvent | FileDeletedEvent) -> None:
        print(event)

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        print(event)

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        print(event)


def session( s ):
    state = State.Main
    
    event_handler = EventHandler(s)
    observer = Observer()
    observer.schedule(event_handler, FILES_PATH, True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

    while True:
        message = szasar.recvline( s ).decode( "ascii" )
        if not message:
            return

        if message.startswith( szasar.Command.List ):
            if state != State.Main:
                sendER( s )
                continue
            try:
                message = "OK\r\n"
                for filename in os.listdir( FILES_PATH ):
                    filesize = os.path.getsize( os.path.join( FILES_PATH, filename ) )
                    message += "{}?{}\r\n".format( filename, filesize )
                message += "\r\n"
            except:
                sendER( s, 2 )
            else:
                s.sendall( message.encode( "ascii" ) )

        elif message.startswith( szasar.Command.Upload ):
            if state != State.Main:
                sendER( s )
                continue
            filename, filesize = message[4:].split('?')
            filesize = int(filesize)
            if filesize > MAX_FILE_SIZE:
                sendER( s, 3 )
                continue
            svfs = os.statvfs( FILES_PATH )
            if filesize + SPACE_MARGIN > svfs.f_bsize * svfs.f_bavail:
                sendER( s, 4 )
                continue
            sendOK( s )
            state = State.Uploading

        elif message.startswith( szasar.Command.Upload2 ):
            if state != State.Uploading:
                sendER( s )
                continue
            state = State.Main
            try:
                with open( os.path.join( FILES_PATH, filename), "wb" ) as f:
                    filedata = szasar.recvall( s, filesize )
                    f.write( filedata )
            except:
                sendER( s, 5 )
            else:
                sendOK( s )

        elif message.startswith( szasar.Command.Delete ):
            if state != State.Main:
                sendER( s )
                continue
            try:
                os.remove( os.path.join( FILES_PATH, message[4:] ) )
            except:
                sendER( s, 6 )
            else:
                sendOK( s )

        elif message.startswith( szasar.Command.Exit ):
            sendOK( s )
            return

        else:
            sendER( s )


if __name__ == "__main__":
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

    s.bind( ('', PORT) )
    s.listen( 5 )

    while True:
        dialog, address = s.accept()
        print( "Conexión aceptada del socket {0[0]}:{0[1]}.".format( address ) )
        s.close()
        session(dialog)
        dialog.close()
        exit( 0 )