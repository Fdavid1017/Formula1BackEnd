from classes.color_scheme import ColorScheme


class Constructor:
    constructor_id = None
    name = '',
    color_scheme = None

    def __init__(self, constructor_id='', name='', color_scheme=ColorScheme()):
        self.color_scheme = color_scheme
        self.name = name
        self.constructor_id = constructor_id

    def serialize(self):
        return {
            'name': self.name,
            'constructor_id': self.constructor_id,
            'color_scheme': self.color_scheme.serialize()
        }
