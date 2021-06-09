class QualifyingResult:
    position = None
    driver = None
    qualifying_1 = None
    qualifying_2 = None
    qualifying_3 = None

    def __init__(self, position, driver, qualifying_1, qualifying_2, qualifying_3):
        self.qualifying_3 = qualifying_3
        self.qualifying_2 = qualifying_2
        self.qualifying_1 = qualifying_1
        self.driver = driver
        self.position = position

    def serialize(self):
        return {
            'qualifying_1': self.qualifying_1,
            'qualifying_2': self.qualifying_2,
            'qualifying_3': self.qualifying_3,
            'driver': self.driver.serialize(),
            'position': self.position
        }
