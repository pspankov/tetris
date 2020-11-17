__version__ = 1.1


def transpose(matrix):
    return list(zip(*matrix))


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.last_row = self.rows - 1
        self.last_col = self.cols - 1
        self.grid = self.create()
        self.i = 0

    def delete_row(self, row):
        del self.grid[row]
        self.grid.insert(0, [0] * self.cols)

    def create(self):
        grid = []
        for row in range(self.rows):
            grid.append([0] * self.cols)
        return grid

    def clear(self):
        self.grid = self.create()

    def __str__(self):
        return self.grid

    def __repr__(self):
        return self.grid

    def __getitem__(self, pos):
        try:
            row, col = pos
            return self.grid[row][col]
        except TypeError:
            return self.grid[pos]

    def __setitem__(self, key, value):
        row, col = key
        self.grid[row][col] = value

    def __iter__(self):
        return iter(self.grid)

    def __next__(self):
        i = self.i
        self.i += 1
        if i <= self.last_row:
            return i
        raise StopIteration
