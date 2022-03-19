import socket

DASHBOARD_IP_ADDRESS = "127.0.0.1"
RECEIVING_PORT = 5555

# Create a listener for new connections on the specified socket
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind((DASHBOARD_IP_ADDRESS, RECEIVING_PORT))
listener.listen(0)

while True:
    sock_conn, sock_addr = listener.accept()
    msg = sock_conn.recv(2048)
    print(msg)