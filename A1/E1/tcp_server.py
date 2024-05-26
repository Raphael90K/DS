import socket
import sys
import threading
import time
import log as l

from msg import receive_msg, send_msg

connected = []
names = []
log = l.Log()
lock = threading.Lock()


def server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_sock:
        s_sock.bind(('127.0.0.1', port))
        s_sock.listen()

        round = threading.Thread(target=play_round)
        round.start()

        com = threading.Thread(target=command)
        com.start()

        while True:
            c_sock, c_address = s_sock.accept()
            lock.acquire()
            rnd, name = receive_msg(c_sock, 10)
            welcome = '<{0}> connected with IP <{1}> on Port <{2}>'.format(name, c_address[0], c_address[1])
            print(welcome)
            connected.append(c_sock)
            names.append(name)

            t = threading.Thread(target=serveClient, args=(c_sock,))
            t.start()
            lock.release()


def play_round():
    while True:
        lock.acquire()
        if len(connected) != 0:
            log.log_round_start(names)
            serverSend('start', log.round_no)
            print(f'round: {log.round_no} - connected: {len(connected)} - start sended')
        lock.release()
        time.sleep(2)


def serveClient(c_sock):
    while True:
        try:
            pass
        except Exception as e:
            print(e)
            if c_sock in connected:
                i = connected.index(c_sock)
                connected.remove(c_sock)
                names.pop(i)
            c_sock.close()
            break


def serverSend(msg, rnd):
    for client in connected:
        try:
            send_msg(client, msg, rnd)
        except Exception as e:
            i = connected.index(client)
            connected.remove(client)
            names.pop(i)
            client.close()
            print(f'error occured, client {client} removed')


def command():
    while True:
        if input() == 'stop':
            lock.acquire()
            try:
                print(len(connected))
                for i in range(len(connected)):
                    client = connected.pop(0)
                    print(f'client {names.pop(0)} i {i} removed')
                    client.close()
                log.create_log()
                print('server stopped')
                print(names)
            except Exception as e:
                print(e)
            lock.release()


def main():
    if len(sys.argv) != 2:
        print("Usage for Server: \"{0}  <port>\"".format(sys.argv[0]))
        sys.exit()
    port = int(sys.argv[1])
    server(port)


if __name__ == '__main__':
    main()
