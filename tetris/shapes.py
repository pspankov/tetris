from tetris import Colors
from tetris.utils import transpose


class Position:
    def __init__(self, row, col):
        self.row = int(row)
        self.col = int(col)

    def __str__(self):
        return f'({self.row}, {self.col})'

    def __repr__(self):
        return f'({self.row}, {self.col})'


class Shape:
    def __init__(self, color, shape):
        self.color = color
        self.shape = shape
        self.set_shape_color()

    @property
    def rows(self):
        return len(self.shape)

    @property
    def cols(self):
        return len(self.shape[0])

    def set_shape_color(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.shape[row][col] != 0:
                    self.shape[row][col] = self.color.value

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


class OBlock(Shape):
    def __init__(self):
        shape = [[1, 1],
                 [1, 1]]
        super().__init__(color=Colors.YELLOW, shape=shape)


class IBlock(Shape):
    def __init__(self):
        shape = [[0, 0, 0, 0],
                 [1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
        super().__init__(color=Colors.LIGHTBLUE, shape=shape)


class TBlock(Shape):
    def __init__(self):
        shape = [[0, 1, 0],
                 [1, 1, 1],
                 [0, 0, 0]]
        super().__init__(color=Colors.PURPLE, shape=shape)


class JBlock(Shape):
    def __init__(self):
        shape = [[1, 0, 0],
                 [1, 1, 1],
                 [0, 0, 0]]
        super().__init__(color=Colors.BLUE, shape=shape)


class LBlock(Shape):
    def __init__(self):
        shape = [[0, 0, 1],
                 [1, 1, 1],
                 [0, 0, 0]]
        super().__init__(color=Colors.ORANGE, shape=shape)


class ZBlock(Shape):
    def __init__(self):
        shape = [[1, 1, 0],
                 [0, 1, 1],
                 [0, 0, 0]]
        super().__init__(color=Colors.RED, shape=shape)


class SBlock(Shape):
    def __init__(self):
        shape = [[0, 1, 1],
                 [1, 1, 0],
                 [0, 0, 0]]
        super().__init__(color=Colors.GREEN, shape=shape)
