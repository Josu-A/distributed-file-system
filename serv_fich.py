#!/usr/bin/env python3

import socket, sys, os, signal
import szasar

PORT = szasar.SERVER_PORT
FILES_PATH = "server_files/"
MAX_FILE_SIZE = 10 * 1 << 20 # 10 MiB
SPACE_MARGIN = 50 * 1 << 20  # 50 MiB


class State:
    Main, Uploading = range(2)


def sendOK(s, params=""):
    s.sendall( ("OK{}\r\n".format( params )).encode("ascii"))


def sendER(s, code=1):
    s.sendall(("ER{}\r\n".format( code )).encode("ascii"))


def session(s):
    state = State.Main
    filename = None
    filesize = 0
    total_bytes_received = 0

    while True:
        message = szasar.recvline(s).decode("ascii")
        if not message:
            return

        if message.startswith(szasar.Command.Upload):
            if state != State.Main:
                sendER(s)
                continue
            filename, filesize = message[4:].split('?')
            filesize = int(filesize)
            if filesize > MAX_FILE_SIZE:
                sendER(s, 3)
                continue
            svfs = os.statvfs(FILES_PATH)
            if filesize + SPACE_MARGIN > svfs.f_bsize * svfs.f_bavail:
                sendER(s, 4)
                continue
            sendOK(s)
            state = State.Uploading
            total_bytes_received = 0

        elif message.startswith(szasar.Command.Upload2):
            if state != State.Uploading:
                sendER(s)
                continue
            offset, chunk_size = map(int, message[4:].split('?'))
            try:
                file_path = os.path.join(FILES_PATH, filename)
                with open(file_path, "r+b") as f:
                    if filesize > 0:
                        f.seek(offset)
                        filedata = szasar.recvall(s, chunk_size)
                        f.write(filedata)
                        total_bytes_received += chunk_size
            except FileNotFoundError:
                with open(file_path, "wb") as f:
                    f.seek(offset)
                    filedata = szasar.recvall(s, chunk_size)
                    f.write(filedata)
                    total_bytes_received += chunk_size
            except:
                sendER(s, 5)
            else:
                sendOK(s)
                if total_bytes_received >= filesize:
                    state = State.Main

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

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:
        dialog, address = s.accept()
        print( "Conexión aceptada del socket {0[0]}:{0[1]}.".format( address ) )
        if( os.fork() ):
            dialog.close()
        else:
            s.close()
            session( dialog )
            dialog.close()
            exit( 0 )
