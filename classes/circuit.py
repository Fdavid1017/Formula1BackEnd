class Circuit:
    id = ''
    name = ''
    city = ''
    country = ''
    image_location = ''
    first_gp = None
    number_of_laps = None
    length = None
    race_distance = None
    gjson_map = ''
    color_scheme = None

    def __init__(self, circuit_id='', name='', city='', country='', image_location='', first_gp='', number_of_laps='',
                 length='', race_distance='',
                 gjson_map='', color_scheme=''):
        self.color_scheme = color_scheme
        self.gjson_map = gjson_map
        self.race_distance = race_distance
        self.length = length
        self.number_of_laps = number_of_laps
        self.first_gp = first_gp
        self.image_location = image_location
        self.country = country
        self.city = city
        self.name = name
        self.circuit_id = circuit_id

    def serialize(self):
        return {
            'color_scheme': self.color_scheme.serialize(),
            'gjson_map': self.gjson_map,
            'race_distance': self.race_distance,
            'length': self.length,
            'number_of_laps': self.number_of_laps,
            'first_gp': self.first_gp,
            'image_location': self.image_location,
            'country': self.country,
            'city': self.city,
            'name': self.name,
            'circuit_id': self.circuit_id
        }
