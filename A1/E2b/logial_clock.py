class LogicalClock:
    def __init__(self):
        self.time = 0

    def __str__(self):
        return f'Localtime: {self.time}'

    def send_event(self, send_function, *args):
        self.time += 1
        send_function(*args, clock=self.time)

    def receive_event(self, receive_function, *args):
        msg, time = receive_function(*args)
        self.time = max(time, self.time + 1)
        return msg
