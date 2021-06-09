class SessionResult:
    position = None
    driver = None
    status = ''
    points = None
    fastest_lap = None

    def __init__(self, position='', driver='', status='', points='', fastest_lap=''):
        self.fastest_lap = fastest_lap
        self.points = points
        self.status = status
        self.driver = driver
        self.position = position

    def serialize(self):
        return {
            'points': self.points,
            'status': self.status,
            'driver': self.driver.serialize(),
            'position': self.position,
            'fastest_lap': self.fastest_lap.serialize()
        }
