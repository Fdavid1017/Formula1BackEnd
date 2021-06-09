class FastestLap:
    rank = None
    lap = None
    time = None
    avg_speed = None

    def __init__(self, rank, lap, time, avg_speed):
        self.avg_speed = avg_speed
        self.time = time
        self.lap = lap
        self.rank = rank

    def serialize(self):
        return {
            'rank': self.rank,
            'lap': self.lap,
            'time': self.time,
            'avg_speed': self.avg_speed
        }
