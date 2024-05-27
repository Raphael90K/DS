import datetime
import random
import socket
import sys
import threading
import time

from msg import *

rand = random.Random()


class Client:
    def __init__(self, ip, port):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.connect((ip, port))

    def start_client(self, id):

        name = f'Cl{id}'
        send_msg(self.c, name)
        t_receive = threading.Thread(target=self.client_play)
        t_receive.start()

    def client_play(self):
        try:
            while True:
                rnd, msg = receive_msg(self.c, 10)
                print(msg)
                print(rnd)
                if msg.strip() == 'start':
                    print(f'start {datetime.datetime.now()}')
                    time.sleep(rand.random() * 3)
                    msg = str(rand.randint(0, 100))
                    send_msg(self.c, msg)
                else:
                    print(f'winner round {rnd}: {msg}')

        except  Exception as e:
            print(f'Chat geschlossen: {e}')
            sys.exit()


def main():
    if len(sys.argv) != 3:
        print("Usage for Client: \"{0}  <ip> <port>\"".format(sys.argv[0]))
        sys.exit()
    ip = sys.argv[1]
    port = int(sys.argv[2])
    c = Client(ip, port)
    c.start_client(1)


if __name__ == '__main__':
    main()
