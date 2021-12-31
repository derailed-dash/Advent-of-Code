class Hexagon:

    # static variables
    vectors = {
        'ne': [1, 1],
        'e': [2, 0],
        'se': [1, -1],
        'sw': [-1, -1],
        'w': [-2, 0],
        'nw': [-1, 1]
    }

    def __init__(self, colour = 'w'):
        # white is default for a tile
        self._colour = colour
    
    def flip(self):
        if self._colour == 'w':
            self._colour = 'b'
        else:
            self._colour = 'w'
        
        return self

    def is_black(self):
        return self._colour == 'b'

    def get_colour(self):
        return self._colour

    def __str__(self):
        return self._colour

    def __repr__(self):
        return f"{self.__class__.__name__}: " + self._colour

    @staticmethod
    def get_vector(compass_direction: str):
        """ Expects a compass direction to be passed.
            I.e. ne, e, se, sw, w, nw
        """
        return Hexagon.vectors[compass_direction]

    @staticmethod
    def get_neighbours(coord):
        ''' Coord passed as [x, y] '''
        neighbours = []

        x = coord[0]
        y = coord[1]

        for vector in Hexagon.vectors.values():
            new_x = x + vector[0]
            new_y = y + vector[1]
            neighbours.append(tuple([new_x, new_y]))

        return neighbours
