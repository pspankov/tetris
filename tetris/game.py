import time
import math
import random
from enum import Enum
from copy import copy
from tetris import Position
from tetris.shapes import Shape


class Collision(Enum):
    LEFT_WALL = 1
    RIGHT_WALL = 2
    FLOOR = 3
    BLOCK = 4


class Tetris:
    # points that correspond to number of lines cleared at the same time
    # 1 line - 40 points
    # 2 lines - 100 points
    # 3 lines - 300 points
    # 4 lines - 1200 points
    POINTS = [40, 100, 300, 1200]

    def __init__(self, grid, shapes_list=None, delay=1):
        self.grid = grid
        if shapes_list is None:
            self.shapes_list = []
            # O-block
            self.shapes_list.append(Shape(id=1, shape=[[1, 1],
                                                       [1, 1]]))
            # I-block
            self.shapes_list.append(Shape(id=2, shape=[[0, 0, 0, 0],
                                                       [2, 2, 2, 2],
                                                       [0, 0, 0, 0],
                                                       [0, 0, 0, 0]]))
            # T-block
            self.shapes_list.append(Shape(id=3, shape=[[0, 3, 0],
                                                       [3, 3, 3],
                                                       [0, 0, 0]]))
            # J-block
            self.shapes_list.append(Shape(id=4, shape=[[4, 0, 0],
                                                       [4, 4, 4],
                                                       [0, 0, 0]]))
            # L-block
            self.shapes_list.append(Shape(id=5, shape=[[0, 0, 5],
                                                       [5, 5, 5],
                                                       [0, 0, 0]]))
            # Z-block
            self.shapes_list.append(Shape(id=6, shape=[[6, 6, 0],
                                                       [0, 6, 6],
                                                       [0, 0, 0]]))
            # S-block
            self.shapes_list.append(Shape(id=7, shape=[[0, 7, 7],
                                                       [7, 7, 0],
                                                       [0, 0, 0]]))
        else:
            self.shapes_list = shapes_list
        self.delay = delay  # the speed of the game (the delay the piece is moved down on it's own)
        self.quit = False
        self.reset_game(clear_grid=False)

    def mainloop(self, delay=True):
        while not self.quit:
            if not self.pause and not self.game_over:
                if self.current_block.can_move:
                    self.move_down()
                self.check_state()
            if delay:
                time.sleep(self.delay)

    def create_block(self) -> Shape:
        # get random shape from all possible shapes
        block = copy(self.shapes_list[random.randint(0, len(self.shapes_list) - 1)])
        # calculate it's position - top center of the grid
        col = math.floor(self.grid.cols / 2) - math.ceil(len(block.shape) / 2)
        block.set_pos(Position(0, col))
        return block

    def set_block(self):
        # set the current block on the grid
        pos = self.current_block.position
        for row in range(self.current_block.rows):
            for col in range(self.current_block.cols):
                if self.current_block.shape[row][col] != 0:
                    self.grid[pos.row + row, pos.col + col] = self.current_block.shape[row][col]

    def remove_block(self):
        # remove the current block from the grid
        if not self.current_block:
            return
        pos = self.current_block.position
        for row in range(self.current_block.rows):
            for col in range(self.current_block.cols):
                if self.current_block.shape[row][col] != 0:
                    self.grid[pos.row + row, pos.col + col] = 0

    def check_state(self):
        lines_cleared = 0
        if not self.current_block.can_move:
            lines_cleared = self.clean_complete_rows()
            self.load_next_blocks()

        return lines_cleared

    def collides(self):
        # set the future position of the block
        # and check if there is already a piece on the grid there
        # along with that check if the block is not off the limits of the grid
        pos = self.current_block.position
        for row in range(self.current_block.rows):
            for col in range(self.current_block.cols):
                if self.current_block.shape[row][col] != 0:
                    if pos.col + col < 0:
                        return Collision.LEFT_WALL
                    elif pos.col + col > self.grid.last_col:
                        return Collision.RIGHT_WALL
                    elif pos.row + row > self.grid.last_row:
                        return Collision.FLOOR
                    elif self.grid[pos.row + row, pos.col + col] != 0:
                        return Collision.BLOCK
        return False

    def clean_complete_rows(self):
        # when row columns are filled we need the clear them out (the rules of the game :))
        lines_cleared = 0
        for row in range(self.grid.rows):
            if 0 not in self.grid[row]:
                lines_cleared += 1
                self.grid.delete_row(row)
        if lines_cleared > 0:
            self.total_lines += lines_cleared
            self.score += self.POINTS[lines_cleared] * (self.level + 1)
        return lines_cleared

    def load_next_blocks(self):
        if self.next_block is None:
            self.next_block = self.create_block()

        self.current_block = self.next_block

        if self.collides():
            self.current_block.can_move = False
            self.game_over = True

        self.set_block()
        self.next_block = self.create_block()

    """ Game options """

    def play_pause(self):
        if not self.game_over:
            self.pause = not self.pause
        else:
            self.reset_game()

    def reset_game(self, clear_grid=True):
        if clear_grid:
            self.grid.clear()

        self.current_block = self.create_block()
        self.set_block()
        self.next_block = self.create_block()
        self.pause = False
        self.game_over = False

        self.score = 0
        self.level = 0
        self.total_lines = 0

    """ Game movements """

    def move_down(self):
        if not self.current_block or not self.current_block.can_move or self.pause:
            return False

        self.remove_block()
        self.current_block.move_down()

        if self.collides():
            self.current_block.move_up()
            self.set_block()
            self.current_block.can_move = False
            return False
        else:
            self.set_block()
            self.score += 1
            return True

    def move_bottom(self):
        while self.current_block.can_move:
            self.move_down()
        return self.check_state()

    def move_left(self, times=1):
        if not self.current_block or not self.current_block.can_move or self.pause:
            return False

        self.remove_block()
        self.current_block.move_left(times)
        if self.collides():
            self.current_block.move_right(times)
            self.set_block()
            return False
        self.set_block()
        return True

    def move_right(self, times=1):
        if not self.current_block or not self.current_block.can_move or self.pause:
            return False

        self.remove_block()
        self.current_block.move_right(times)
        if self.collides():
            self.current_block.move_left(times)
            self.set_block()
            return False
        self.set_block()
        return True

    def rotate(self):
        if not self.current_block or not self.current_block.can_move or self.pause:
            return False

        self.remove_block()
        self.current_block.rotate()

        # fix cases where block can't rotate if all the way to the left or right

        # if block is next to left wall move to the right and then rotate
        collision = self.collides()
        if collision == Collision.LEFT_WALL:
            for i in range(self.current_block.cols):
                self.current_block.move_right()
                if not self.collides():
                    break

        # if block is next to right wall move to the left and then rotate
        if collision == Collision.RIGHT_WALL:
            for i in range(self.current_block.cols):
                self.current_block.move_left()
                if not self.collides():
                    break

        if self.collides():
            # rotating 3 times returns it to it's original position
            self.current_block.rotate(3)
            self.set_block()
            return False

        self.set_block()
        return True
