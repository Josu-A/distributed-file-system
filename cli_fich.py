#!/usr/bin/env python3

import socket, sys, os
import szasar

SERVER_FILES = 'localhost'
PORT_FILES = 6012
SERVER_WD = 'localhost'
PORT_WD = 6013

ER_MSG = (
    "Correcto.",
    "Comando desconocido o inesperado.",
    "Error al crear la lista de ficheros.",
    "El fichero es demasiado grande.",
    "Error al preparar el fichero para subirlo.",
    "Error al subir el fichero.",
    "Error al borrar el fichero." )


class Actions:
    Upload, Delete, Exit = range( 1, 4 )
    Options = ( "Subir fichero", "Borrar fichero", "Salir" )


def iserror( message ):
    if( message.startswith( "ER" ) ):
        code = int( message[2:] )
        print( ER_MSG[code] )
        return True
    else:
        return False


def int2bytes( n ):
    if n < 1 << 10:
        return str(n) + " B  "
    elif n < 1 << 20:
        return str(round( n / (1 << 10) ) ) + " KiB"
    elif n < 1 << 30:
        return str(round( n / (1 << 20) ) ) + " MiB"
    else:
        return str(round( n / (1 << 30) ) ) + " GiB"


if __name__ == "__main__":
    if len( sys.argv ) > 5:
        print( "Usage: {} [<files_server> [<files_port> [<watchdog_server> [<watchdog_port>]]]]".format( sys.argv[0] ) )
        exit( 2 )

    if len( sys.argv ) >= 2:
        SERVER_FILES = sys.argv[1]
    if len( sys.argv ) >= 3:
        PORT_FILES = int( sys.argv[2])
    if len( sys.argv ) >= 4:
        SERVER_WD = sys.argv[3]
    if len( sys.argv ) == 5:
        PORT_WD = int( sys.argv[4])

    sf = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sf.connect( (SERVER_FILES, PORT_FILES) )

    sw = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    sw.connect( (SERVER_WD, PORT_WD) )

    while True:
        # Get option from the watchdog server
        event = szasar.recvline( sw ).decode("ascii")

        if event.startswith("EFCR"):
            filename = event[4:]
            filesize = 0
            message = f"{szasar.Command.Upload}{filename}?{filesize}\r\n"
            sf.sendall(message.encode("ascii"))
            message = szasar.recvline(sf).decode("ascii")
            if iserror(message):
                continue
            
            message = f"{szasar.Command.Upload2}\r\n"
            sf.sendall(message.encode("ascii"))
            sf.sendall(b'')
            message = szasar.recvline(sf).decode("ascii")
            if not iserror( message ):
                print(f"Empty file {filename} uploaded correctly.")


    sf.close()
