class FastestLap:
    lap = None
    time = None
    avg_speed = None

    def __init__(self, lap='', time='', avg_speed=''):
        self.avg_speed = avg_speed
        self.time = time
        self.lap = lap

    def serialize(self):
        return {
            'lap': self.lap,
            'time': self.time,
            'avg_speed': self.avg_speed
        }
