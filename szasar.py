CLIENT_FILES_PATH = "client_files/"
WATCHDOG_PORT = 6013
SERVER_PORT = 6012

class Command:
	Upload, Upload2, Delete, Move, Exit = ("UPLO", "UPL2", "DELE", "MOVE", "EXIT")

def recvline(s, removeEOL = True):
	line = b''
	CRreceived = False
	while True:
		c = s.recv(1)
		if c == b'':
			raise EOFError("Connection closed by the peer before receiving an EOL.")
		line += c
		if c == b'\r':
			CRreceived = True
		elif c == b'\n' and CRreceived:
			if removeEOL:
				return line[:-2]
			else:
				return line
		else:
			CRreceived = False

def recvall(s, size):
	message = b''
	while(len(message) < size):
		chunk = s.recv(size - len(message))
		if chunk == b'':
			raise EOFError("Connection closed by the peer before receiving the requested {} bytes.".format(size))
		message += chunk
	return message
