# Monitoring-Module
### Setup
#### Flask
1. Install waitress: ```pip install flask```
2. Install socketio: ```pip install python-socketio```
3. [WINDOWS] Install TShark from this website: https://www.wireshark.org/download.html
##### OR
3. [LINUX] Install TShark: ```sudo apt install tshark```
4. Install PyShark: ```pip install pyshark```

#### Gunicorn/Waitress
1. [WINDOWS] Install waitress: ```pip install waitress```
##### OR
1. [LINUX] Install gunicorn ```pip install gunicorn```
2. Install socketio: ```pip install python-socketio```
3. [WINDOWS] Install TShark from this website: https://www.wireshark.org/download.html
##### OR
3. [LINUX] Install TShark: ```sudo apt install tshark```
4. Install PyShark: ```pip install pyshark``

### Run
#### Flask
1. cd into the directory containing main.py 
2. [WINDOWS] Type the command: ```py main.py``` and press [ENTER]
##### OR
2. [LINUX] Type the command: ```sudo main.py``` and press [ENTER]

#### Gunicorn/Waitress
1. cd into the directory containing app.py
2. [WINDOWS] Type the command ```waitress-serve --threads=50 --listen=127.0.0.1:5555 app:app```
##### OR
2. [LINUX] Type the command ```sudo gunicorn --threads 50 -b '127.0.0.1:5555' app:app```
