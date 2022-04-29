from flask import Flask
import socketio
from scapy.all import *

ADDRESS = "localhost"
PORT = 5555
DEBUG = True


def main():
    # Create a listener for new connections on the specified socket
    sio = socketio.Server(logger=DEBUG, engineio_logger=False, async_mode='threading',
                          cors_allowed_origins='http://localhost:3000')
    app = Flask(__name__)
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

    # TODO: add way to track whether threads for specific ports should be alive?
    daemon_dict = {}

    # Define function to be called when there is a start message
    @sio.on('start')
    def start_monitor_thread(sid, port):
        if DEBUG:
            print("Received start:\n" +
                  "sid: " + str(sid) + "\n" +
                  "port: " + str(port))
        # TODO: may want to add error checking to this to ensure the msg is a properly formatted port number
        port_number = str(port)

        if (str(sid), str(port)) in daemon_dict:
            if daemon_dict[(str(sid), str(port))]:
                # A thread for this already exists so skip creating it
                if DEBUG:
                    print("WARNING: daemon already exists with tuple: (" + str(sid) + ", " + str(port) + ")")
                return

        daemon_dict[(str(sid), str(port))] = True
        if DEBUG:
            print("daemon_dict: " + str(daemon_dict))

        # Call the monitor function and send to dashboard in a loop
        while daemon_dict[(str(sid), str(port))]:
            metrics = process_packets(port=port_number)
            # Convert metrics and stream identifier to JSON and send to dashboard
            new_msg = {
                "metrics": metrics,
                "stream_id": port_number
            }
            if DEBUG:
                print("Sending to " + str(ADDRESS) + " on port " + str(PORT) + ":\n" + str(new_msg) + "\n")
            sio.emit(port_number, new_msg, room=sid)

        if DEBUG:
            print("daemon ending with tuple: (" + str(sid) + ", " + str(port) + ")")

    @sio.on('stop')
    def start_monitor_thread(sid, port):
        if DEBUG:
            print("Received stop:\n" +
                  "sid: " + str(sid) + "\n" +
                  "port: " + str(port))
        daemon_dict[(str(sid), str(port))] = False
        if DEBUG:
            print("daemon_dict: " + str(daemon_dict))

    @sio.event
    def disconnect(sid):
        print("Received stop:\n" +
              "sid: " + str(sid))
        for (sid, port) in daemon_dict:
            daemon_dict[(sid, port)] = False

    if DEBUG:
        print("Listening to " + str(ADDRESS) + " on port " + str(PORT) + "\n")

    if __name__ == '__main__':
        app.run(port=PORT)


# driving function to process data throughput of a specified port/interface.
# Port: Port used to filter packets received from the interface
def process_packets(port):
    packet_filter = 'port ' + port
    capture = sniff(iface='lo', filter=packet_filter, timeout=2)

    data_received = 0
    if len(capture) == 0:
        return 0

    for i in range(0, len(capture)):
        data_received = data_received + len(capture[i])
    return  { 'data_transfer_rate': data_received, 'packets_per_second': len(capture) }


main()
