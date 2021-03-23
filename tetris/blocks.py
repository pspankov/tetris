import random
from tetris import transpose


class Tetrimino:
    def __init__(self, id, name, shape):
        self.id = id
        self.name = name
        self.shape = shape
        self.height = len(self.shape)
        self.width = len(self.shape[0])
        self.can_move = True
        self.col = 0
        self.row = 0

    def move(self, col, row):
        self.col += col
        self.row += row

    def rotate(self, times=1):
        for time in range(times):
            self.shape = transpose(self.shape)
            for i in range(self.width):
                self.shape[i] = list(self.shape[i])[::-1]

    def __str__(self):
        return f'({self.col}, {self.row}) {self.name}'

    def __repr__(self):
        return f'({self.col}, {self.row}) {self.name}'


class Bag:
    def __init__(self):
        self.blocks = []

    def add_blocks(self):
        self.blocks = [
            Tetrimino(id=1, name='O-Block', shape=[[1, 1],
                                                   [1, 1]]),
            Tetrimino(id=2, name='I-Block', shape=[[0, 0, 0, 0],
                                                   [2, 2, 2, 2],
                                                   [0, 0, 0, 0],
                                                   [0, 0, 0, 0]]),
            Tetrimino(id=3, name='T-Block', shape=[[0, 3, 0],
                                                   [3, 3, 3],
                                                   [0, 0, 0]]),
            Tetrimino(id=4, name='J-Block', shape=[[4, 0, 0],
                                                   [4, 4, 4],
                                                   [0, 0, 0]]),
            Tetrimino(id=5, name='L-Block', shape=[[0, 0, 5],
                                                   [5, 5, 5],
                                                   [0, 0, 0]]),
            Tetrimino(id=6, name='Z-Block', shape=[[6, 6, 0],
                                                   [0, 6, 6],
                                                   [0, 0, 0]]),
            Tetrimino(id=7, name='S-Block', shape=[[0, 7, 7],
                                                   [7, 7, 0],
                                                   [0, 0, 0]])
        ]
        return self.blocks

    def shuffle(self):
        random.shuffle(self.blocks)
        return self.blocks

    def fill(self):
        self.add_blocks()
        self.shuffle()
        return self.blocks

    def empty(self):
        self.blocks = []
