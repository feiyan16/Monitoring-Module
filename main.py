from threading import Thread
import socketio
import json
import pyshark
import eventlet

ADDRESS = "localhost"
PORT = 5555
DEBUG = True


def main():
    # Create a listener for new connections on the specified socket
    sio = socketio.Server(logger=True, cors_allowed_origins='http://localhost:3000')

    # Define function to be called when there is a start message
    @sio.on('start')
    def start_monitor_thread(sid, data):
        if DEBUG:
            print('sid:', sid)
            print('data:' + str(data))
        stream_thread = Thread(target=monitor_stream, args=(sio, data))
        stream_thread.daemon = True
        stream_thread.start()

    if DEBUG:
        print("Listening to " + str(ADDRESS) + " on port " + str(PORT) + "\n")

    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('localhost', PORT)), app)


def monitor_stream(sio, port):
    # TODO: may want to add error checking to this to ensure the msg is a properly formatted port number
    port_number = str(port)

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
            print("Sending to " + str(ADDRESS) + " on port " + str(PORT) + ":\n" + str(new_msg) + "\n")
        new_msg = bytes(new_msg, 'utf-8')
        sio.emit(port_number, new_msg)


# driving function to process data throughput of a specified port/interface.
# Port: Port used to filter packets received from the interface
def process_packets(port):
    packet_filter = 'port ' + port
    capture = pyshark.LiveCapture(interface='lo', bpf_filter=packet_filter)

    capture.sniff(timeout=2)
    data_received = 0
    print(capture)
    if len(capture) == 0:
        return 0

    for i in range(0, len(capture)):
        data_received = data_received + int(capture[i].length)
    return data_received


main()
