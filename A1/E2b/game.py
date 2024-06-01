import threading

from log import Log


class Game:
    def __init__(self):
        self.lock = threading.Lock()
        self.rnd = 0
        self.last_start = 0
        self.last_end = 1000
        self.throws = []  # [[name, throw]]

    def increase_start(self, time):
        with self.lock:
            self.last_start = time

    def increase_end(self, time):
        with self.lock:
            self.last_end = time

    def get_last_start(self):
        with self.lock:
            return self.last_start

    def get_last_end(self):
        with self.lock:
            return self.last_end

    def add_throw(self, name, score, client_time):
        with self.lock:
            self.throws.append([name, score, client_time])

    def start_round(self, log: Log, names, time):
        with self.lock:
            self.rnd += 1
            log.log_round_start(self.rnd, names, time)

    def end_round(self, log: Log, round_end_time):
        with self.lock:
            if len(self.throws) > 0:
                winner = max(self.throws, key=lambda x: x[1])
                log.log_round_end(self.throws, winner, round_end_time)
                self.throws = []
                return winner
            else:
                log.log_round_end(self.throws, ["", 0], round_end_time)
                return ["", 0]
