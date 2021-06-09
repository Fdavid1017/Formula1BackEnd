class SessionResultsGroup:
    session_dateTime = None
    results = []

    def __init__(self, session_datetime='', results=''):
        self.results = results
        self.session_dateTime = session_datetime

    def serialize(self):
        result = []

        for i in range(len(self.results)):
            r = self.results[i]
            result.append(r.serialize())

        return {
            'session_dateTime': self.session_dateTime,
            'results': result
        }
