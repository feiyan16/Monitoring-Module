import pyshark
import sys

if len(sys.argv) == 1:
	print('Parameters missing: <interface> <optional: bpf_filter>')
	sys.exit(0)

# default
capture = None

if len(sys.argv) == 3:
	capture = pyshark.LiveCapture(interface=sys.argv[1].strip(), bpf_filter=sys.argv[2].strip())
elif len(sys.argv) == 2:
	capture = pyshark.LiveCapture(interface=sys.argv[1].strip())

for packet in capture.sniff_continuously():
	print('size:', packet.length)