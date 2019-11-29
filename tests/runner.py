import time
import sys
sys.path.insert(0, '../')
from tasks import start_received_request_action


rcv_msg_1 = {
    "link": "http://releases.ubuntu.com/18.04.3/ubuntu-18.04.3-live-server-amd64.iso?_ga=2.215748887.1611994196.1575046610-1346832950.1573937065",
    "filename": "sys_1",
    "extension": "iso",
    "download_dir": "/home/kuba/",
    "action": "download_request"
    }

rcv_msg_2 = {
    "link": "http://releases.ubuntu.com/18.04.3/ubuntu-18.04.3-live-server-amd64.iso?_ga=2.189396139.1611994196.1575046610-1346832950.1573937065",
    "filename": "sys_2",
    "extension": "iso",
    "download_dir": "/home/kuba/",
    "action": "download_request"
    }

rcv_msg_3 = {
    "link": "http://cdimage.ubuntu.com/kubuntu/releases/19.10/release/kubuntu-19.10-desktop-amd64.iso",
    "filename": "sys_2",
    "extension": "iso",
    "download_dir": "/",
    "action": "check_status"
    }


assert start_received_request_action(rcv_msg_1)["response"] == "download task started"
print("1 Passed")
assert start_received_request_action(rcv_msg_2)["response"] == "download task started"
print("2 Passed")
print("Wait 30 seconds to check if downloading starts")
time.sleep(20)
assert not start_received_request_action(rcv_msg_3)["sys_1"]["status"] == "0.0"
assert not start_received_request_action(rcv_msg_3)["sys_2"]["status"] == "0.0"
print("Quick test passed")
