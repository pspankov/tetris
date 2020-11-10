from tetris import Position, transpose


class Shape:
    def __init__(self, id, shape):
        self.id = id
        self.shape = shape
        self.can_move = True

    @property
    def rows(self):
        return len(self.shape)

    @property
    def cols(self):
        return len(self.shape[0])

    def set_pos(self, pos: Position):
        self.position = pos

    def move_left(self, times=1):
        self.position.col -= times

    def move_right(self, times=1):
        self.position.col += times

    def move_up(self):
        self.position.row -= 1

    def move_down(self):
        self.position.row += 1

    def rotate(self, times=1):
        for time in range(times):
            self.shape = transpose(self.shape)
            for i in range(len(self.shape)):
                self.shape[i] = list(self.shape[i])[::-1]
