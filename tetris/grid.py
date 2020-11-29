import math
import random
from enum import Enum

from copy import deepcopy
from tetris import transpose


class Collision(Enum):
    LEFT_WALL = 1
    RIGHT_WALL = 2
    FLOOR = 3
    BLOCK = 4


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
    @staticmethod
    def create():
        return [
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

    @staticmethod
    def random():
        bag = Bag.create()
        random.shuffle(bag)
        return bag


class Grid:
    def __init__(self, rows, cols, bag: Bag):
        self.rows = rows
        self.cols = cols
        self.last_row = self.rows - 1
        self.last_col = self.cols - 1
        self.i = 0
        self.bag = bag
        self.reset()

    def create(self):
        return [[0 for col in range(self.cols)] for row in range(self.rows)]

    def get(self, row, col):
        return self.grid[row][col]

    def delete_row(self, row):
        self.grid.pop(row)
        self.grid.insert(0, [0] * self.cols)

    def reset(self):
        self.grid = self.create()
        self.tetriminos = None
        self.block = None
        self.next_block = None
        self.create_block()

    def create_block(self):
        if not self.tetriminos:
            self.tetriminos = self.bag.random()

        if self.next_block is None:
            self.block = self.tetriminos.pop()
        else:
            self.block = self.next_block

        # calculate it's position - top center of the grid
        col = math.floor(self.cols / 2) - math.ceil(self.block.width / 2)
        self.block.col = col
        self.next_block = self.tetriminos.pop()
        self.set_block()

        return self.block

    def set_block(self):
        # set the current block on the grid
        for row in range(self.block.height):
            for col in range(self.block.width):
                if self.block.shape[row][col] != 0:
                    self.grid[self.block.row + row][self.block.col + col] = self.block.shape[row][col]

    def remove_block(self):
        # remove the current block from the grid
        if not self.block:
            return

        for row in range(self.block.height):
            for col in range(self.block.width):
                if self.block.shape[row][col] != 0:
                    self.grid[self.block.row + row][self.block.col + col] = 0

    def collides(self):
        # set the future position of the block
        # and check if there is already a piece on the grid there
        # along with that check if the block is not off the limits of the grid
        for row in range(self.block.height):
            for col in range(self.block.width):
                if self.block.shape[row][col] != 0:
                    if self.block.col + col < 0:
                        return Collision.LEFT_WALL
                    elif self.block.col + col > self.last_col:
                        return Collision.RIGHT_WALL
                    elif self.block.row + row > self.last_row:
                        return Collision.FLOOR
                    elif self.grid[self.block.row + row][self.block.col + col] != 0:
                        return Collision.BLOCK
        return False

    """ Game movements """

    def move(self, col=0, row=0):
        if not self.block.can_move:
            return

        self.remove_block()
        self.block.move(col, row)

        if self.collides():
            self.block.move(-col, -row)
            self.set_block()
            if col == 0:  # if it's moved down
                self.block.can_move = False
            return False
        else:
            self.set_block()
            return True

    def rotate(self):
        if not self.block.can_move:
            return

        self.remove_block()
        self.block.rotate()

        # fix cases where block can't rotate if all the way to the left or right

        # if block is next to left wall move to the right and then rotate
        collision = self.collides()
        if collision == Collision.LEFT_WALL:
            for i in range(self.block.width):
                self.block.move(1, 0)
                if not self.collides():
                    break

        # if block is next to right wall move to the left and then rotate
        if collision == Collision.RIGHT_WALL:
            for i in range(self.block.width):
                self.block.move(-1, 0)
                if not self.collides():
                    break

        if self.collides():
            # rotating 3 times returns it to it's original position
            self.block.rotate(3)
            self.set_block()
            return False

        self.set_block()
        return True

    def __getitem__(self, row):
        return self.grid[row]

    def __setitem__(self, key, value):
        row, col = key
        self.grid[row][col] = value
