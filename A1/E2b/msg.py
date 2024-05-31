import socket


def receive_msg(sock: socket.socket, length: int = 10):
    msg: bytes = b''
    received = 0
    while received < length:
        part = sock.recv(1)
        received += len(part)
        msg += part
    msg_time = int.from_bytes(msg[:2])
    msg_decode = msg[2:].decode('ascii')
    msg_decode.strip()
    return msg_decode, msg_time


def send_msg(sock: socket.socket, msg: str, length: int = 10, clock=0):
    clock = clock.to_bytes(2)
    msg = fix_bytes_length(msg, length - 2)
    msg = clock + msg
    sock.sendall(msg)


def fix_bytes_length(s, length=8):
    encoded = s.encode('ascii')

    if len(encoded) > length:
        return encoded[:length]
    else:
        return encoded.rjust(length, b' ')
