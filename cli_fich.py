#!/usr/bin/env python3

import socket, sys, os
import szasar

SERVER = 'localhost'
PORT = 6012
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
	if len( sys.argv ) > 3:
		print( "Uso: {} [<servidor> [<puerto>]]".format( sys.argv[0] ) )
		exit( 2 )

	if len( sys.argv ) >= 2:
		SERVER = sys.argv[1]
	if len( sys.argv ) == 3:
		PORT = int( sys.argv[2])

	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	s.connect( (SERVER, PORT) )

	while True:
		# Get option from the watchdog server
		# option = 

		if option == Actions.Upload:
			filename = input( "Indica el fichero que quieres subir: " )
			try:
				filesize = os.path.getsize( filename )
				with open( filename, "rb" ) as f:
					filedata = f.read()
			except:
				print( "No se ha podido acceder al fichero {}.".format( filename ) )
				continue

			message = "{}{}?{}\r\n".format( szasar.Command.Upload, filename, filesize )
			s.sendall( message.encode( "ascii" ) )
			message = szasar.recvline( s ).decode( "ascii" )
			if iserror( message ):
				continue

			message = "{}\r\n".format( szasar.Command.Upload2 )
			s.sendall( message.encode( "ascii" ) )
			s.sendall( filedata )
			message = szasar.recvline( s ).decode( "ascii" )
			if not iserror( message ):
				print( "El fichero {} se ha enviado correctamente.".format( filename ) )

		elif option == Actions.Delete:
			filename = input( "Indica el fichero que quieres borrar: " )
			message = "{}{}\r\n".format( szasar.Command.Delete, filename )
			s.sendall( message.encode( "ascii" ) )
			message = szasar.recvline( s ).decode( "ascii" )
			if not iserror( message ):
				print( "El fichero {} se ha borrado correctamente.".format( filename ) )

		elif option == Actions.Exit:
			message = "{}\r\n".format( szasar.Command.Exit )
			s.sendall( message.encode( "ascii" ) )
			message = szasar.recvline( s ).decode( "ascii" )
			break
	s.close()
