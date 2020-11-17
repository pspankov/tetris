from tetris import transpose


class Shape:
    def __init__(self, id, shape):
        self.id = id
        self.shape = shape
        self.can_move = True
        self.row = 0
        self.col = 0

    @property
    def height(self):
        return len(self.shape)

    @property
    def width(self):
        return len(self.shape[0])

    def move_left(self, times=1):
        self.col -= times

    def move_right(self, times=1):
        self.col += times

    def move_up(self):
        self.row -= 1

    def move_down(self):
        self.row += 1

    def rotate(self, times=1):
        for time in range(times):
            self.shape = transpose(self.shape)
            for i in range(len(self.shape)):
                self.shape[i] = list(self.shape[i])[::-1]

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)
