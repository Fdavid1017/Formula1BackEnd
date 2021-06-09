class FreePracticeResult:
    position = None
    driver = None
    fastest_lap = None

    def __init__(self, position='', driver='', fastest_lap=''):
        self.fastest_lap = fastest_lap
        self.driver = driver
        self.position = position

    def serialize(self):
        return {
            'driver': self.driver.serialize(),
            'position': self.position,
            'fastest_lap': self.fastest_lap.serialize()
        }
