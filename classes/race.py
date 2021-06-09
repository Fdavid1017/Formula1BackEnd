import datetime


class Race:
    race_round = None
    race_name = ''
    circuit = None
    date_time = datetime.datetime.now

    def __init__(self, race_round='', race_name='', circuit='', date_time=''):
        self.date_time = date_time
        self.circuit = circuit
        self.race_name = race_name
        self.race_round = race_round

    def serialize(self):
        return {
            'date_time': self.date_time,
            'circuit': self.circuit.serialize(),
            'race_name': self.race_name,
            'race_round': self.race_round
        }
