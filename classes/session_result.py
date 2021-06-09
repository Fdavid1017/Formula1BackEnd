class SessionResult:
    position = None
    driver = None
    status = ''
    points = None

    def __init__(self, position, driver, status, points):
        self.points = points
        self.status = status
        self.driver = driver
        self.position = position

    def serialize(self):
        return {
            'points': self.points,
            'status': self.status,
            'driver': self.driver,
            'position': self.position
        }
