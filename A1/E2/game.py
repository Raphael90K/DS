import threading

from A1.E2.log import Log


class Game:
    def __init__(self):
        self.lock = threading.Lock()
        self.rnd = 0
        self.dice = []  # [[name, score]]

    def add_throw(self, name, score):
        with self.lock:
            self.dice.append([name, score])

    def start_round(self, log: Log, names):
        with self.lock:
            self.rnd += 1
            log.log_round_start(self.rnd, names)

    def end_round(self, log: Log):
        with self.lock:
            if len(self.dice) > 0:
                winner = max(self.dice, key=lambda x: x[1])
                log.log_round_end(self.dice, winner)
                self.dice = []
                return winner
            else:
                log.log_round_end(self.dice, ["", 0])
                return ["", 0]
