from enum import Enum


class Collision(Enum):
    LEFT_WALL = 1
    RIGHT_WALL = 2
    FLOOR = 3
    BLOCK = 4


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.last_row = self.rows - 1
        self.last_col = self.cols - 1
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

    def set_block(self, block):
        for row in range(block.height):
            for col in range(block.width):
                if block.shape[row][col] != 0:
                    self.grid[block.row + row][block.col + col] = block.shape[row][col]

    def remove_block(self, block):
        for row in range(block.height):
            for col in range(block.width):
                if block.shape[row][col] != 0:
                    self.grid[block.row + row][block.col + col] = 0

    def collides(self, block):
        # set the future position of the block
        # and check if there is already a piece on the grid there
        # along with that check if the block is not off the limits of the grid
        for row in range(block.height):
            for col in range(block.width):
                if block.shape[row][col] != 0:
                    if block.col + col < 0:
                        return Collision.LEFT_WALL
                    elif block.col + col > self.last_col:
                        return Collision.RIGHT_WALL
                    elif block.row + row > self.last_row:
                        return Collision.FLOOR
                    elif self.grid[block.row + row][block.col + col] != 0:
                        return Collision.BLOCK
        return False

    def __getitem__(self, row):
        return self.grid[row]

    def __setitem__(self, key, value):
        row, col = key
        self.grid[row][col] = value
