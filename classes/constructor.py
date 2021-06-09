class Constructor:
    constructor_id = None
    name = ''

    def __init__(self, constructor_id='', name=''):
        self.name = name
        self.constructor_id = constructor_id

    def serialize(self):
        return {
            'name': self.name,
            'constructor_id': self.constructor_id
        }
