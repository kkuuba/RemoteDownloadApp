import socket
import json

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 8555

# connect to the server on local computer
s.connect(("127.0.0.1", port))

# receive data from the server
data = {
    "link": "http://cdimage.ubuntu.com/kubuntu/releases/19.10/release/kubuntu-19.10-desktop-amd64.iso",
    "filename": "ubuntu_image",
    "extension": "iso",
    "download_dir": "/home/kuba/",
    "action": "check_status"
}


obj = json.dumps(data).encode("utf-8")
s.send(obj)
resp = s.recv(4096).decode("utf-8")
print(resp)
s.close()
