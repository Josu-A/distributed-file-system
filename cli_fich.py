#!/usr/bin/env python3

import socket, sys, os
import szasar

SERVER_FILES = 'localhost'
PORT_FILES = szasar.SERVER_PORT
SERVER_WD = 'localhost'
PORT_WD = szasar.WATCHDOG_PORT
FILES_PATH = szasar.CLIENT_FILES_PATH

ER_MSG = (
    "Correcto.",
    "Comando desconocido o inesperado.",
    "Error al crear la lista de ficheros.",
    "El fichero es demasiado grande.",
    "Error al preparar el fichero para subirlo.",
    "Error al subir el fichero.",
    "Error al borrar el fichero.",
    "Error al mover el fichero")


class Actions:
    Upload, Delete, Exit = range(1, 4)
    Options = ("Subir fichero", "Borrar fichero", "Salir")


def iserror(message):
    if(message.startswith("ER")):
        code = int(message[2:])
        print(ER_MSG[code])
        return True
    else:
        return False


def int2bytes(n):
    if n < 1 << 10:
        return str(n) + " B  "
    elif n < 1 << 20:
        return str(round(n / (1 << 10))) + " KiB"
    elif n < 1 << 30:
        return str(round(n / (1 << 20))) + " MiB"
    else:
        return str(round(n / (1 << 30))) + " GiB"


if __name__ == "__main__":
    if len(sys.argv) > 5:
        print("Usage: {} [<files_server> [<files_port> [<watchdog_server> [<watchdog_port>]]]]".format(sys.argv[0]))
        exit(2)

    if len(sys.argv) >= 2:
        SERVER_FILES = sys.argv[1]
    if len(sys.argv) >= 3:
        PORT_FILES = int(sys.argv[2])
    if len(sys.argv) >= 4:
        SERVER_WD = sys.argv[3]
    if len(sys.argv) == 5:
        PORT_WD = int(sys.argv[4])

    sf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sf.connect((SERVER_FILES, PORT_FILES))

    sw = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    sw.connect((SERVER_WD, PORT_WD))

    while True:
        # Get option from the watchdog server
        event = szasar.recvline(sw).decode("ascii")

        if event.startswith("FIMD"):
            filepath, filesize = event[4:].split('?')
            filename = filepath.removeprefix(FILES_PATH)
            filesize = int(filesize)
            try:
                with open(filepath, "rb") as f:
                    filedata = f.read()
            except:
                print(f"Error trying to access the file {filepath}.")
                continue

            message = f"{szasar.Command.Upload}{filename}?{filesize}\r\n"
            sf.sendall(message.encode("ascii"))
            message = szasar.recvline(sf).decode("ascii")
            if iserror(message):
                continue

            message = f"{szasar.Command.Upload2}\r\n"
            sf.sendall(message.encode("ascii"))
            sf.sendall(filedata)
            message = szasar.recvline(sf).decode("ascii")
            if not iserror(message):
                print(f"File {filepath} uploaded correctly.")

        elif event.startswith("FIDL"):
            filepath = event[4:]
            filename = filepath.removeprefix(FILES_PATH)

            message = f"{szasar.Command.Delete}{filename}\r\n"
            sf.sendall(message.encode("ascii"))
            message = szasar.recvline(sf).decode("ascii")
            if not iserror(message):
                print(f"File {filepath} deleted correctly.")

        elif event.startswith("FIMV"):
            filepath_src, filepath_dest = event[4:].split('?')
            filename_src = filepath_src.removeprefix(FILES_PATH)
            filename_dest = filepath_dest.removeprefix(FILES_PATH)
            try:
                open(filepath_dest, "rb").close()
            except:
                print(f"Error trying to access the file {filepath_dest}.")
                continue

            message = f"{szasar.Command.Move}{filename_src}?{filename_dest}\r\n"
            sf.sendall(message.encode("ascii"))
            message = szasar.recvline(sf).decode("ascii")
            if not iserror(message):
                print(f"File {filepath_src} correctly moved to {filepath_dest}.")

    sf.close()
