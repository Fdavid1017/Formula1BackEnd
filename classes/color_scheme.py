class ColorScheme:
    primary = '#fffff'
    secondary = '#fffff'
    tertiary = '#fffff'

    def __init__(self, primary, secondary, tertiary):
        self.tertiary = tertiary
        self.secondary = secondary
        self.primary = primary

    def serialize(self):
        return {
            'tertiary': self.tertiary,
            'secondary': self.secondary,
            'primary': self.primary
        }
