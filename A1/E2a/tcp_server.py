import os
import socket
import sys
import threading
import time
import log as lg
from game import Game

from msg import receive_msg, send_msg


class Server:
    def __init__(self, DAUER_DER_RUNDE, LOGNAME):
        self.connected = []
        self.names = []
        self.log = lg.Log(LOGNAME, DAUER_DER_RUNDE)
        self.lock = threading.Lock()
        self.game = Game()
        self.DAUER_DER_RUNDE = DAUER_DER_RUNDE
        self.WARTEZEIT = 2

    def serve(self, ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_sock:
            s_sock.bind((ip, port))
            s_sock.listen()

            rnd = threading.Thread(target=self.play_round, daemon=True)
            rnd.start()

            stop_flag = threading.Event()
            com = threading.Thread(target=self.command, args=(stop_flag, s_sock), daemon=True)
            com.start()

            while not stop_flag.is_set():
                c_sock, c_address = s_sock.accept()
                self.lock.acquire()
                name, clock = receive_msg(c_sock, 10)
                welcome = '<{0}> connected with IP <{1}> on Port <{2}>'.format(name, c_address[0], c_address[1])
                print(welcome)
                self.connected.append(c_sock)
                self.names.append(name.strip())

                t = threading.Thread(target=self.serve_client, args=(c_sock, name), daemon=True)
                t.start()
                self.lock.release()

    def play_round(self):
        while True:
            self.lock.acquire()
            if len(self.connected) != 0:
                # round start
                self.game.start_round(self.log, self.names)
                self.server_send('start')
                print(f'round: {self.game.rnd} - connected: {len(self.connected)} - start sended')
                self.lock.release()
                time.sleep(self.DAUER_DER_RUNDE)

                # round end
                self.lock.acquire()
                winner = self.game.end_round(self.log)
                self.server_send('stop')
                print(f'round: {self.game.rnd} - connected: {len(self.connected)} - end send')

                # waiting for next round
                time.sleep(self.WARTEZEIT)
                self.game.await_next_round(self.log)
                self.log.refresh()
            self.lock.release()

    def serve_client(self, c_sock, name):
        while True:
            try:
                msg, clock = receive_msg(c_sock, 10)
                throw = int(msg.strip())
                self.game.add_throw(name, throw)
            except Exception as e:
                print(e)
                if c_sock in self.connected:
                    i = self.connected.index(c_sock)
                    self.connected.remove(c_sock)
                    self.names.pop(i)
                c_sock.close()
                break

    def server_send(self, msg, clock=0):
        for client in self.connected:
            try:
                send_msg(client, msg, clock=clock)
            except Exception as e:
                i = self.connected.index(client)
                self.connected.remove(client)
                self.names.pop(i)
                client.close()
                print(f'error occured, client {client} removed')

    def command(self, stop_flag: threading.Event, s_sock: socket.socket):
        while True:
            if input() == 'stop':
                self.lock.acquire()
                try:
                    for i in range(len(self.connected)):
                        client = self.connected.pop(0)
                        print(f'client {self.names.pop(0)} i {i} removed')
                        client.close()
                    print('server stopped')
                except Exception as e:
                    print(e)
                finally:
                    self.log.create_log()
                    self.lock.release()
                    print('server beendet')
                    stop_flag.set()
                    os._exit(0)


def main():
    if len(sys.argv) != 5:
        print("Usage for Server: \"{0}  <ip> <port> <DAUER_DER_RUNDE> <LOGNAME>\"".format(sys.argv[0]))
        sys.exit()
    ip = sys.argv[1]
    port = int(sys.argv[2])
    server = Server(float(sys.argv[3]), sys.argv[4])

    server.serve(ip, port)


if __name__ == '__main__':
    main()
