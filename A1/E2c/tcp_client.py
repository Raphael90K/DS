import datetime
import random
import socket
import sys
import threading
import time

from logial_clock import LogicalClock
from msg import *

rand = random.Random()


class Client:
    def __init__(self, ip, port, SPIELER_LATENZ):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.connect((ip, port))
        self.LATENZ = SPIELER_LATENZ

        self.clock = LogicalClock()

    def start_client(self, id):

        name = f'Cl{id}'
        self.clock.send_event(send_msg, self.c, name)
        t_receive = threading.Thread(target=self.client_play)
        t_receive.start()

    def client_play(self):
        try:
            stops = []
            while True:
                msg, server_time = self.clock.receive_event(receive_msg, self.c)
                stop_received = threading.Event()
                stops.append(stop_received)
                if msg.strip() == 'stop':
                    for stop in stops:
                        stop.set()
                    stops = []
                    print(f'round stopped at {server_time}')

                elif msg.strip() == 'start':
                    print(f'start round at {server_time}')
                    roll = threading.Thread(target=self.roll_dice, args=(stop_received,))
                    roll.start()

        except  Exception as e:
            print(f'Chat geschlossen: {e}')
            sys.exit()

    def roll_dice(self, stop_received: threading.Event):
        time.sleep(rand.random() * self.LATENZ)
        WURF = str(rand.randint(0, 100))

        if not stop_received.is_set():
            self.clock.send_event(send_msg, self.c, WURF)
        else:
            print(f'{threading.current_thread()} too late')


def main():
    if len(sys.argv) != 4:
        print("Usage for Client: \"{0}  <ip> <port> <SPIELER_LATENZ>\"".format(sys.argv[0]))
        sys.exit()
    ip = sys.argv[1]
    port = int(sys.argv[2])
    c = Client(ip, port, float(sys.argv[3]))
    c.start_client(1)


if __name__ == '__main__':
    main()
