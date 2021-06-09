class DriverStanding:
    position = None
    points = None
    wins = None
    driver = None

    def __init__(self, position, points, wins, driver):
        self.driver = driver
        self.wins = wins
        self.points = points
        self.position = position

    def serialize(self):
        return {
            'driver': self.driver.serialize(),
            'wins': self.wins,
            'points': self.points,
            'position': self.position
        }
