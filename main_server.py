from tasks import Task
import time

plik_1 = Task("http://releases.ubuntu.com/18.04.3/ubuntu-18.04.3-desktop-amd64.iso?_ga=2.125916238.21998216.1574890477-1346832950.1573937065", "sys_1","iso", "/home/kuba/")
plik_2 = Task("https://zorinos.com/download/15/core/64", "sys_2","iso", "/home/kuba/")
while True:
    print(plik_1.show_task())
    print(plik_2.show_task())
    time.sleep(1)
