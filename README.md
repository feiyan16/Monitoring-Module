# Monitoring-Module
### Setup
1. Install wireshark, https://www.wireshark.org/download.html
2. Install PyShark, https://pypi.org/project/pyshark/
NOTE: As long as you install them and get pyshark running, you're good, it doesn't have to be from these websites.
### Run
1. cd into the directory containing sniff.py
2. Type the command: ```python3 sniff.py <interface> <opt: bpf-filter>``` and press [ENTER]
#### Parameters
The paramters are interface and bpf-filter, interface is mandatory, but bpf-filter is optional
##### Interface
The default is 'lo0' (loopback), but you can also refer to https://www.juniper.net/documentation/us/en/software/junos/interfaces-security-devices/topics/topic-map/security-interface-intro.html#id-understanding-interfaces for more interfaces
##### Bpf-filter
Refer to https://www.ibm.com/docs/en/qsip/7.4?topic=queries-berkeley-packet-filters for information on filters
3. If you haven't already, in the browser, go to localhost:8080 and make sure the simulator is running
4. You should see numbers appear, like so: <img width="573" alt="image" src="https://user-images.githubusercontent.com/55895535/156860737-47f6b2a7-5c27-412a-832e-ad848255e100.png">
