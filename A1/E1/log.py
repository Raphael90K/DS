import datetime
import json


class Log:
    def __init__(self):
        self.log = {'starting time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'rounds': []}

        self.round_no = 0

    def log_round_start(self, names: list):
        if len(names) != 0:
            round = {'round': self.round_no,
                     'starting_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     'connected': str(names)}
            self.log['rounds'].append(round)

            self.round_no += 1

    def create_log(self, file: str = 'log.json'):
        final_log = json.dumps(self.log, indent=4)
        with open(file, 'w') as f:
            f.write(final_log)
