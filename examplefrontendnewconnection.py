import socket                   # Socket Programming support

HOST_ADDRESS = "127.0.0.1"    # Servers address (0.0.0.0 for generic access)
HOST_PORT = 4444            # Servers port (Used in client scripts for connection to server)
DEBUG = True

test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # TCP socket creation
test.connect((HOST_ADDRESS, HOST_PORT))
test.send(b"This is a test. It should tell us the port number for a new connection.")
