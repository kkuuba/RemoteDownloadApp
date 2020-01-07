import socket
import json
import time

"""
Some Test Cases to check if our script is still working.
BEFORE RUN TESTS ------>>> SERVER.PY HAVE TO BE RUNNING.
"""

msg_1 = {
    "link": "http://releases.ubuntu.com/18.04.3/ubuntu-18.04.3-live-server-amd64.iso?_ga=2.215748887.1611994196.1575046610-1346832950.1573937065",
    "filename": "sys_1",
    "extension": "iso",
    "download_dir": "/home/kuba/",
    "action": "download_request"
}

msg_2 = {
    "link": "http://releases.ubuntu.com/18.04.3/ubuntu-18.04.3-live-server-amd64.iso?_ga=2.189396139.1611994196.1575046610-1346832950.1573937065",
    "filename": "sys_2",
    "extension": "iso",
    "download_dir": "/home/kuba/",
    "action": "download_request"
}

msg_3 = {
    "link": "http://cdimage.ubuntu.com/kubuntu/releases/19.10/release/kubuntu-19.10-desktop-amd64.iso",
    "filename": "sys_2",
    "extension": "iso",
    "download_dir": "/",
    "action": "check_status"
}

port = 8555
#############################################################################
# TestCase 1
#############################################################################
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(("127.0.0.1", port))
s.send(json.dumps(msg_1).encode("utf-8"))
resp_1 = json.loads(s.recv(4096).decode("utf-8"))
print(resp_1)
s.close()
assert resp_1["response"] == "download task started"
print("TestCase 1 ----------> passed\n")
#############################################################################
# TestCase 2
#############################################################################
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(("127.0.0.1", port))
s.send(json.dumps(msg_2).encode("utf-8"))
resp_2 = json.loads(s.recv(4096).decode("utf-8"))
print(resp_2)
s.close()
assert resp_1["response"] == "download task started"
print("TestCase 2 ----------> passed\n")
#############################################################################
# TestCase 3
#############################################################################
print("Wait 20 seconds to check if downloading starts")
time.sleep(20)
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(("127.0.0.1", port))
s.send(json.dumps(msg_3).encode("utf-8"))
resp_3 = json.loads(s.recv(4096).decode("utf-8"))
print(resp_3)
s.close()
assert not resp_3["sys_1"]["status"] == "0.0"
print(resp_3["sys_1"]["status"])
assert not resp_3["sys_2"]["status"] == "0.0"
print(resp_3["sys_2"]["status"])
print("TestCase 3 ----------> passed\n")
print("_____________All TCs passed_____________\n")
