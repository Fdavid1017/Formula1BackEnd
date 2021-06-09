class Driver:
    driver_id = ''
    driver_number = None
    code = ''
    given_name = ''
    family_name = ''
    constructor = None

    def __init__(self, driver_id, number, code, given_name, family_name, constructor):
        self.constructor = constructor
        self.family_name = family_name
        self.given_name = given_name
        self.code = code
        self.number = number
        self.driver_id = driver_id

    def serialize(self):
        return {
            'constructor': self.constructor.serialize(),
            'family_name': self.family_name,
            'given_name': self.given_name,
            'code': self.code,
            'number': self.number,
            'driver_id': self.driver_id
        }
