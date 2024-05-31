import copy
import datetime
import json


class Log:
    def __init__(self, LOGNAME, DAUER_DER_RUNDE):
        self.LOGNAME = LOGNAME
        self.log = {'starting_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'round_duration': DAUER_DER_RUNDE,
                    'rounds': []}
        self.rnd = {}

    def log_round_start(self, round_no, names: list, clock_time):
        self.rnd = {'round': round_no,
                    'starting_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'logical_start' : clock_time,
                    'connected': copy.deepcopy(names)}

    def log_late_throws(self, late, clock_time):
        self.rnd['late_throws'] = copy.deepcopy(late)
        self.rnd['logical_waiting_end'] = clock_time

    def log_round_end(self, participants, winner, clock_time):
        self.rnd['ending_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.rnd['logical_end'] = clock_time
        self.rnd['participants'] = copy.deepcopy(participants)
        self.rnd['winner'] = copy.deepcopy(winner)

    def refresh(self):
        self.log['rounds'].append(copy.deepcopy(self.rnd))
        self.rnd = {}

    def create_log(self):
        final_log = json.dumps(self.log, indent=4)
        with open(f'{self.LOGNAME}.json', 'w') as f:
            f.write(final_log)
        print('log created')
