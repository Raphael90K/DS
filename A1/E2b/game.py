import threading

from log import Log


class Game:
    def __init__(self):
        self.lock = threading.Lock()
        self.rnd = 0
        self.throws = []  # [[name, throw]]

    def add_throw(self, name, score):
        with self.lock:
            self.throws.append([name, score])

    def start_round(self, log: Log, names, clock_time):
        with self.lock:
            self.rnd += 1
            log.log_round_start(self.rnd, names, clock_time)

    def end_round(self, log: Log, clock_time):
        with self.lock:
            if len(self.throws) > 0:
                winner = max(self.throws, key=lambda x: x[1])
                log.log_round_end(self.throws, winner, clock_time)
                self.throws = []
                return winner
            else:
                log.log_round_end(self.throws, ["", 0], clock_time)
                return ["", 0]

    def await_next_round(self, log: Log, clock_time):
        with self.lock:
            log.log_late_throws(self.throws, clock_time)
            self.throws = []