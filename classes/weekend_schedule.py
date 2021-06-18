class WeekendSchedule:
    pf1: None
    fp2: None
    fp3: None
    qualifying: None
    race: None

    def __init__(self, fp1, fp2, fp3, qualifying, race):
        self.race = race
        self.qualifying = qualifying
        self.fp3 = fp3
        self.fp2 = fp2
        self.fp1 = fp1

    def serialize(self):
        return {
            'fp1': self.fp1,
            'fp2': self.fp2,
            'fp3': self.fp3,
            'qualifying': self.qualifying,
            'race': self.race
        }
