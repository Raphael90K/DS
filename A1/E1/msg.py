import socket


def receive_msg(sock: socket.socket, length: int):
    msg: bytes = b''
    received = 0
    while received < length:
        part = sock.recv(1)
        received += len(part)
        msg += part

    return msg
