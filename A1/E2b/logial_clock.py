import threading


class LogicalClock:
    def __init__(self):
        self.time = 0
        self.lock = threading.Lock()

    def __str__(self):
        return f'Localtime: {self.time}'

    def send_event(self, send_function, *args):
        with self.lock:
            self.time += 1
            send_function(*args, clock=self.time)

    def receive_event(self, receive_function, *args):
        with self.lock:
            msg, client_time = receive_function(*args)
            self.time = max(client_time, self.time + 1)
            return msg, client_time
