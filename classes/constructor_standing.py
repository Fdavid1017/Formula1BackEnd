class ConstructorStanding:
    position = None
    points = None
    wins = None
    constructor = None

    def __init__(self, position='', points='', wins='', constructor=''):
        self.constructor = constructor
        self.wins = wins
        self.points = points
        self.position = position

    def serialize(self):
        return {
            'constructor': self.constructor.serialize(),
            'wins': self.wins,
            'points': self.points,
            'position': self.position
        }
