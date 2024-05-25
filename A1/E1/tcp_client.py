import datetime
import random
import socket
import sys
import threading
import time

from msg import *

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rand = random.Random()


def client(ip, port):
    c.connect((ip, port))
    name = 'Hallo   '.encode('ascii')
    c.sendall(name)

    t_send = threading.Thread(target=clientSend)
    t_send.start()

    t_receive = threading.Thread(target=clientReceive)
    t_receive.start()


def clientReceive():
    try:
        while True:
            msg = receive_msg(c, 5)
            if msg.decode('ascii') == 'start':
                print(f'start {datetime.datetime.now()}')
    except:
        print("Chat geschlossen")
        sys.exit()


# Methode zum Versenden von Nachrichten
def clientSend():
    while True:
        msg = input()
        new_msg = msg.encode('ascii')
        c.sendall(new_msg)
        if msg.lower() == 'stop':
            print("Chat verlassen")
            c.close()
            break


def main():
    if len(sys.argv) != 3:
        print("Usage for Client: \"{0}  <ip> <port>\"".format(sys.argv[0]))
        sys.exit()
    ip = sys.argv[1]
    port = int(sys.argv[2])
    client(ip, port)


if __name__ == '__main__':
    main()
