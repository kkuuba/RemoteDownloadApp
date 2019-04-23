# -*- coding: utf-8 -*-
import socket
from utilities import task_parser


def send(msg):  # sending messege to client

    msg = msg.encode("utf-8")
    connection.sendall(msg)


sock = socket.socket(

    socket.AF_INET,  # sockets stuff
    socket.SOCK_STREAM  #

)

forbidden = "00.23.00.23.002"  # somebody have no luck

try:

    server_address = ("192.168.0.50", 6555)
    print('starting up on %s port %s' % server_address)

    sock.bind(server_address)

    sock.listen(1)  # listening on this port

except:

    server_address = ("192.168.0.105", 6555)  # or on this eventualyy ...
    print('starting up on %s port %s' % server_address)

    sock.bind(server_address)

    sock.listen(1)

while True:

    print('waiting for a connection')
    connection, client_address = sock.accept()

    # someone connected get data from him

    if client_address[0] == forbidden[0]:  # shield from huge trafiic very basic shield

        continue

    print("connection from", client_address)

    licznik = 0

    send('Enter your task:\n')

    while True:
        # can you speak polish ?
        data = connection.recv(4096)  # <- odbieramy 16 bajtów danych
        data = data.decode("utf-8")  # <- dekodujemy bajty do Unicode
        # Jeśli przesłane są dane -> odsyłamy spowrotem
        if data:

            dane = data.split("#@#")

            if dane[0] == "1234":

                send(task_parser(dane[1]))
                send("Enter task:\n")


            else:

                send("Incorrect key\nEnter task:\n")

            if licznik > 10:

                send("To many entry attempts\n")
                forbidden = client_address

                break

            else:

                licznik = licznik + 1

        else:

            print("closing connection\n", client_address)

            break
