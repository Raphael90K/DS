import socket


def receive_msg(sock: socket.socket, length: int = 10):
    msg: bytes = b''
    received = 0
    while received < length:
        part = sock.recv(1)
        received += len(part)
        msg += part

    round = int.from_bytes(msg[:2])
    msg_decode = msg[2:].decode('ascii')
    msg_decode.strip()
    return round, msg_decode


def send_msg(sock: socket.socket, msg: str, length: int = 10, rnd=0):
    try:
        rnd = rnd.to_bytes(2)
        msg = fix_bytes_length(msg, length - 2)
        msg = rnd + msg
        print(msg)
        sock.sendall(msg)
        return True
    except socket.error:
        return False


def fix_bytes_length(s, length=8):
    encoded = s.encode('ascii')

    if len(encoded) > length:
        return encoded[:length]
    else:
        return encoded.rjust(length, b'\x00')
