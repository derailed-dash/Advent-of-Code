class Tile:
    def __init__(self, data: list):
        # list of strings
        self._data = data
        self._edges = self.init_edges()
    
    def get_data(self):
        """ Returns the tile as a list of strings """
        return self._data

    def get_inner(self):
        new_data = []
        for row in self.get_data()[1:-1]:
            new_row = row[1:-1]
            new_data.append(new_row)

        return new_data

    def init_edges(self):
        top = self.get_data()[0]
        bottom = self.get_data()[-1]

        left = []
        right = []
        
        for row in self.get_data():
            left.append(row[0])
            right.append(row[-1])

        return [top, "".join(right), bottom, "".join(left)]

    def get_edges(self):
        return self._edges

    def get_top_edge(self):
        return self._edges[0]

    def get_right_edge(self):
        return self._edges[1]
    
    def get_bottom_edge(self):
        return self._edges[2]
    
    def get_left_edge(self):
        return self._edges[3]       

    def __eq__(self, other):
        return self.get_data() == other.get_data()

    def __hash__(self):
        return hash(self.get_data())

    def __str__(self):
        return "\n".join(line for line in self.get_data())

    def __repr__(self):
        return "Tile: " + self.__str__()

    def flip_x(self):
        new_tile_rows = []
        
        for row in self.get_data():
            new_row = row[::-1]
            new_tile_rows.append(new_row)

        return Tile(new_tile_rows)

    def flip_y(self):
        return Tile(self.get_data()[::-1])

    def rotate_90(self):
        new_tile_rows = []

        for i in range(len(self.get_data())):
            new_row = []
            for row in self.get_data()[::-1]:
                new_row.append(row[i])

            new_tile_rows.append("".join(new_row))
        
        return Tile(new_tile_rows)
            
    def rotate_180(self):
        return self.flip_y().flip_x()

    def get_configurations(self):
        # This is costly.  Match edges before trying combos

        configurations = []
        configurations.append(self)
        configurations.append(self.flip_x())
        configurations.append(self.flip_y())

        rotated_90 = self.rotate_90()
        configurations.append(rotated_90)
        configurations.append(rotated_90.flip_y())
        configurations.append(rotated_90.flip_x())

        rotated_180 = self.rotate_180()
        configurations.append(rotated_180)
        configurations.append(rotated_180.flip_y())
        configurations.append(rotated_180.flip_x())

        rotated_270 = rotated_180.rotate_90()
        configurations.append(rotated_270)
        configurations.append(rotated_270.flip_y())
        configurations.append(rotated_270.flip_x())
    
        return configurations

    def get_edge_values(self):
        # This is the quick way of checking if a tile has a matching edge
        # return numeric val of edges and reversed edges
        edge_values = []
        for edge in self.get_edges():
            binary_edge = edge.replace(".", "0").replace("#", "1")
            edge_values.append(int(binary_edge, 2))

            binary_edge = edge[::-1].replace(".", "0").replace("#", "1")
            edge_values.append(int(binary_edge, 2))

        return edge_values

    @staticmethod
    def edge_value(edge):
        binary_edge = edge.replace(".", "0").replace("#", "1")
        return int(binary_edge, 2)   