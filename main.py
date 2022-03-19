from threading import Thread
import socket
import json
import pyshark

DASHBOARD_IP_ADDRESS = "127.0.0.1"
RECEIVING_PORT = 4444
SENDING_PORT = 5555
DEBUG = True

# Create a listener for new connections on the specified socket
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind((DASHBOARD_IP_ADDRESS, RECEIVING_PORT))
listener.listen(0)

if DEBUG:
    print("Listening to " + str(DASHBOARD_IP_ADDRESS) + " on port " + str(RECEIVING_PORT) + "\n")


def monitor_stream(recv_sock_connection):
    # Get the port number to monitor from the front end
    msg = recv_sock_connection.recv(2048)
    # TODO: may want to add error checking to this to ensure the msg is a properly formatted port number
    port_number = str(msg)

    # Create a connection to send data metrics over
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender.connect((DASHBOARD_IP_ADDRESS, SENDING_PORT))

    if DEBUG:
        print("Sending to " + str(DASHBOARD_IP_ADDRESS) + " on port " + str(SENDING_PORT) + "\n")

    # Call the monitor function and send to dashboard in a loop
    while True:
        metrics = process_packets(port=port_number)
        # Convert metrics and stream identifier to JSON and send to dashboard
        new_msg = {
            "metrics": metrics,
            "stream_id": port_number
        }
        new_msg = json.dumps(new_msg)
        if DEBUG:
            print("Sending: " + str(new_msg) + "\n")
        new_msg = bytes(new_msg, 'utf-8')
        sender.send(new_msg)

#driving function to process data throughput of a specificed port/interface.
	# Port: Port used to filter packets received from the interface
def process_packets(port):
	filter = 'port ' + port
	capture = pyshark.LiveCapture(interface='lo', bpf_filter=filter)

	capture.sniff(timeout=2)
	dataReceived = 0
	print(capture)
	if len(capture) == 0:
		return 0
	
	for i in range(0, len(capture)):
		dataReceived = dataReceived + int(capture[i].length)
	return dataReceived


while True:
    listener_sock_connection, listener_sock_addr = listener.accept()  # Accept new connections
    stream_thread = Thread(target=monitor_stream,
                           args=(listener_sock_connection,))  # Start thread for new connections
    stream_thread.daemon = True
    stream_thread.start()
