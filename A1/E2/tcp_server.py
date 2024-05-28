import socket
import sys
import threading
import time
import log as lg
from A1.E2.game import Game

from msg import receive_msg, send_msg


class Server:
    def __init__(self):
        self.connected = []
        self.names = []
        self.log = lg.Log()
        self.lock = threading.Lock()
        self.game = Game()

    def serve(self, ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_sock:
            s_sock.bind((ip, port))
            s_sock.listen()

            rnd = threading.Thread(target=self.play_round)
            rnd.start()

            com = threading.Thread(target=self.command)
            com.start()

            while True:
                c_sock, c_address = s_sock.accept()
                self.lock.acquire()
                rnd, name = receive_msg(c_sock, 10)
                welcome = '<{0}> connected with IP <{1}> on Port <{2}>'.format(name, c_address[0], c_address[1])
                print(welcome)
                self.connected.append(c_sock)
                self.names.append(name)

                t = threading.Thread(target=self.serve_client, args=(c_sock, name))
                t.start()
                self.lock.release()

    def play_round(self):
        while True:
            self.lock.acquire()
            if len(self.connected) != 0:
                self.game.start_round(self.log, self.names)
                self.server_send('start', self.game.rnd)
                print(f'round: {self.game.rnd} - connected: {len(self.connected)} - start sended')
                self.lock.release()
                time.sleep(2)
                self.lock.acquire()
                winner = self.game.end_round(self.log)
                self.server_send(winner[0], self.game.rnd)
                print(f'round: {self.game.rnd} - connected: {len(self.connected)} - end send')
            self.lock.release()

    def serve_client(self, c_sock, name):
        while True:
            try:
                rnd, msg = receive_msg(c_sock, 10)
                score = int(msg.strip())
                self.game.add_throw(name, score)
            except Exception as e:
                print(e)
                if c_sock in self.connected:
                    i = self.connected.index(c_sock)
                    self.connected.remove(c_sock)
                    self.names.pop(i)
                c_sock.close()
                break

    def server_send(self, msg, rnd):
        for client in self.connected:
            try:
                send_msg(client, msg, rnd=rnd)
            except Exception as e:
                i = self.connected.index(client)
                self.connected.remove(client)
                self.names.pop(i)
                client.close()
                print(f'error occured, client {client} removed')

    def command(self):
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
                    sys.exit()


def main():
    if len(sys.argv) != 2:
        print("Usage for Server: \"{0}  <port>\"".format(sys.argv[0]))
        sys.exit()
    port = int(sys.argv[1])
    server = Server()
    server.serve('127.0.0.1', port)


if __name__ == '__main__':
    main()
