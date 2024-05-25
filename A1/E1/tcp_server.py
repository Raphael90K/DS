import socket
import sys
import threading
import time

from msg import receive_msg

connected = []
names = []


# Starts server
def server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_sock:
        s_sock.bind(('127.0.0.1', port))
        s_sock.listen()

        while True:
            c_sock, c_address = s_sock.accept()
            name = receive_msg(c_sock, 8).decode()
            welcome = '<{0}> connected with IP <{1}> on Port <{2}>'.format(name, c_address[0], c_address[1])
            print(welcome)
            connected.append(c_sock)
            names.append(name)

            t = threading.Thread(target=serveClient, args=(c_sock,))
            t.start()


def serveClient(c_sock):
    while True:
        try:
            serverSend('start'.encode('ascii'), None)
            print('start sended')
            time.sleep(2)
        except:
            print("serve Client error")
            if c_sock in connected:
                i = connected.index(c_sock)
                connected.remove(c_sock)
                names.pop(i)
            c_sock.close()
            break


def serverSend(msg, c_sock):
    for client in connected:
        print(f'client {client}')
        try:
            if client == c_sock:
                continue
            client.sendall(msg)
        except Exception as e:
            print(e)
            i = connected.index(client)
            connected.remove(client)
            names.pop(i)
            client.close()


# Methode zur Formatierung der Nachrichten gem. Vorgabe vor Weiterleitung
def msg_format(name, msg):
    return bytearray().join((name.encode("ascii"), ":".encode("ascii"), msg.encode("ascii")))


def main():
    if len(sys.argv) != 2:
        print("Usage for Server: \"{0}  <port>\"".format(sys.argv[0]))
        sys.exit()
    port = int(sys.argv[1])
    server(port)


if __name__ == '__main__':
    main()
