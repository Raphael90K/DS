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

    def log_round_start(self, round_no, names: list):
        self.rnd = {'round': round_no,
                    'starting_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'connected': copy.deepcopy(names)}

    def log_late_throw(self, name, throw, client_time):
        for i, rnd in enumerate(self.log['rounds']):
            if client_time <= rnd['logical_ending']:
                self.log['rounds'][i]['late_throws'].append([name, throw])

    def log_round_end(self, participants, winner, round_end_time):
        self.rnd['ending_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.rnd['logical_ending'] = round_end_time
        self.rnd['participants'] = copy.deepcopy(participants)
        self.rnd['winner'] = copy.deepcopy(winner)
        self.rnd['late_throws'] = []

    def refresh(self):
        self.log['rounds'].append(copy.deepcopy(self.rnd))
        self.rnd = {}

    def create_log(self):
        final_log = json.dumps(self.log, indent=4)
        with open(f'{self.LOGNAME}.json', 'w') as f:
            f.write(final_log)
        print('log created')
