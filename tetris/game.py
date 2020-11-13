import time
import math
import random
from enum import Enum
from copy import deepcopy
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
        self.shapes_list = self.create_shapes() if shapes_list is None else shapes_list

        self.delay = delay  # the speed of the game (the delay the piece is moved down on it's own)

        self.pause = False
        self.game_over = False
        self.quit = False

        self.score = 0
        self.level = 0
        self.lines = 0

        self.bag = None
        self.block = None
        self.next_block = None
        self.create_block()

    def create_shapes(self):
        shapes_list = []
        # O-block
        shapes_list.append(Shape(id=1, shape=[[1, 1],
                                              [1, 1]]))
        # I-block
        shapes_list.append(Shape(id=2, shape=[[0, 0, 0, 0],
                                              [2, 2, 2, 2],
                                              [0, 0, 0, 0],
                                              [0, 0, 0, 0]]))
        # T-block
        shapes_list.append(Shape(id=3, shape=[[0, 3, 0],
                                              [3, 3, 3],
                                              [0, 0, 0]]))
        # J-block
        shapes_list.append(Shape(id=4, shape=[[4, 0, 0],
                                              [4, 4, 4],
                                              [0, 0, 0]]))
        # L-block
        shapes_list.append(Shape(id=5, shape=[[0, 0, 5],
                                              [5, 5, 5],
                                              [0, 0, 0]]))
        # Z-block
        shapes_list.append(Shape(id=6, shape=[[6, 6, 0],
                                              [0, 6, 6],
                                              [0, 0, 0]]))
        # S-block
        shapes_list.append(Shape(id=7, shape=[[0, 7, 7],
                                              [7, 7, 0],
                                              [0, 0, 0]]))

        return shapes_list

    def get_random_bag(self):
        bag = deepcopy(self.shapes_list)
        random.shuffle(bag)
        return bag

    def create_block(self):
        # get random shape from all possible shapes
        if not self.bag:
            self.bag = self.get_random_bag()

        if self.next_block is None:
            self.block = self.bag.pop()
        else:
            self.block = self.next_block

        # calculate it's position - top center of the grid
        col = math.floor(self.grid.cols / 2) - math.ceil(len(self.block.shape) / 2)
        self.block.set_pos(Position(0, col))
        self.next_block = self.bag.pop()

        return self.block

    def mainloop(self, delay=True):
        while not self.quit:
            if not self.pause and not self.game_over:
                if self.block.can_move:
                    self.move_down(score=False)
                self.check_state()
            if delay:
                time.sleep(self.delay)

    def set_block(self):
        # set the current block on the grid
        pos = self.block.position
        for row in range(self.block.rows):
            for col in range(self.block.cols):
                if self.block.shape[row][col] != 0:
                    self.grid[pos.row + row, pos.col + col] = self.block.shape[row][col]

    def remove_block(self):
        # remove the current block from the grid
        if not self.block:
            return
        pos = self.block.position
        for row in range(self.block.rows):
            for col in range(self.block.cols):
                if self.block.shape[row][col] != 0:
                    self.grid[pos.row + row, pos.col + col] = 0

    def check_state(self):
        lines_cleared = 0
        if not self.block.can_move:
            lines_cleared = self.clean_complete_rows()
            self.create_block()
            # if collides immediately after creation - we reached the top - it's game over
            if self.collides():
                self.game_over = True
            else:
                self.set_block()

        return lines_cleared

    def collides(self):
        # set the future position of the block
        # and check if there is already a piece on the grid there
        # along with that check if the block is not off the limits of the grid
        pos = self.block.position
        for row in range(self.block.rows):
            for col in range(self.block.cols):
                if self.block.shape[row][col] != 0:
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
            self.lines += lines_cleared
            self.score += self.POINTS[lines_cleared] * (self.level + 1)
        return lines_cleared

    """ Game options """

    def play_pause(self):
        if not self.game_over:
            self.pause = not self.pause
        else:
            self.reset_game()

    def reset_game(self):
        self.grid.clear()
        self.pause = False
        self.game_over = False

        self.score = 0
        self.level = 0
        self.lines = 0

        self.bag = None
        self.block = None
        self.next_block = None
        self.create_block()
        self.set_block()

    """ Game movements """

    def move_down(self, score=True):
        if not self.block or not self.block.can_move or self.pause:
            return False

        self.remove_block()
        self.block.move_down()

        if self.collides():
            self.block.move_up()
            self.set_block()
            self.block.can_move = False
            return False
        else:
            self.set_block()
            if score:
                self.score += 1
            return True

    def drop(self, check_state=True):
        """ Drop block all way down """
        while self.block.can_move:
            self.move_down()
        if check_state:
            return self.check_state()

    def move_left(self, times=1):
        if not self.block or not self.block.can_move or self.pause:
            return False

        self.remove_block()
        self.block.move_left(times)
        if self.collides():
            self.block.move_right(times)
            self.set_block()
            return False
        self.set_block()
        return True

    def move_right(self, times=1):
        if not self.block or not self.block.can_move or self.pause:
            return False

        self.remove_block()
        self.block.move_right(times)
        if self.collides():
            self.block.move_left(times)
            self.set_block()
            return False
        self.set_block()
        return True

    def rotate(self):
        if not self.block or not self.block.can_move or self.pause:
            return False

        self.remove_block()
        self.block.rotate()

        # fix cases where block can't rotate if all the way to the left or right

        # if block is next to left wall move to the right and then rotate
        collision = self.collides()
        if collision == Collision.LEFT_WALL:
            for i in range(self.block.cols):
                self.block.move_right()
                if not self.collides():
                    break

        # if block is next to right wall move to the left and then rotate
        if collision == Collision.RIGHT_WALL:
            for i in range(self.block.cols):
                self.block.move_left()
                if not self.collides():
                    break

        if self.collides():
            # rotating 3 times returns it to it's original position
            self.block.rotate(3)
            self.set_block()
            return False

        self.set_block()
        return True
