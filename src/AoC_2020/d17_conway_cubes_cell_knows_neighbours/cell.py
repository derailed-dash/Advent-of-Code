class Cell:
    def __init__(self, coords: list):
        self._coords = tuple(coords)

    def get_coords(self):
        return self._coords

    def get_x(self):
        return self.get_coords()[0]

    def get_y(self):
        return self.get_coords()[1]

    def get_z(self):
        return self.get_coords()[2]

    def __str__(self):
        return ", ".join(str(coord) for coord in self.get_coords())

    def __repr__(self):
        return (f"{self.__class__.__name__}: ") + ", ".join(str(coord) for coord in self.get_coords()) 

    def __eq__(self, other):
        return self.get_coords() == other.get_coords()
    
    def __hash__(self):
        # coords are a tuple.  So return hash of tuple.
        # we need this if we want to use things like "in <iterator>"
        return hash(self.get_coords())

    def get_neighbours(self):
        neighbours = [Cell([self.get_x()+x, self.get_y()+y, self.get_z()+z]) 
                        for x in range(-1, 2) 
                        for y in range(-1, 2) 
                        for z in range(-1, 2) 
                        if not (x == 0 and y == 0 and z == 0)]

        return neighbours


class Cell4d(Cell):
    def get_w(self):
        return self.get_coords()[3]

    def get_neighbours(self):
        # override
        neighbours = [Cell4d([self.get_x()+x, self.get_y()+y, self.get_z()+z, self.get_w()+w]) 
                        for x in range(-1, 2) 
                        for y in range(-1, 2) 
                        for z in range(-1, 2)
                        for w in range(-1, 2) 
                        if not (x == 0 and y == 0 and z == 0 and w == 0)]

        return neighbours
