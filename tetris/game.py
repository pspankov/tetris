import time
import math
import random
from itertools import dropwhile
from tetris import Position
from tetris.shapes import Shape, OBlock, IBlock, LBlock, JBlock, SBlock, ZBlock, TBlock
from tetris.utils import transpose


class Tetris:
    # points that correspond to number of lines cleared at the same time
    # 1 line - 40 points
    # 2 lines - 100 points
    # 3 lines - 300 points
    # 4 lines - 1200 points
    POINTS = [40, 100, 300, 1200]

    def __init__(self, grid, shapes_list=None):
        self.grid = grid
        self.shapes_list = [OBlock, IBlock, LBlock, JBlock, SBlock, ZBlock, TBlock] \
            if shapes_list is None else shapes_list
        self.delay = 1  # that's basically the speed of the game or what is the time between the piece is moved down
        self.quit = False
        self.reset_game(clear_grid=False)

    def run(self, delay=True):
        if not self.pause:
            if self.current_block is None:
                self.load_next_blocks()
            elif not self.move_down():
                if self.current_block.position.row <= 0:
                    self.game_over = True

                self.clean_complete_rows()
                self.current_block = None
                self.load_next_blocks()
        if delay:
            time.sleep(self.delay)

    def mainloop(self):
        while not self.quit:
            self.run()

    def play_pause(self):
        if not self.game_over:
            self.pause = not self.pause
        else:
            self.reset_game()

    def reset_game(self, clear_grid=True):
        if clear_grid:
            self.grid.clear()

        self.current_block = None
        self.next_block = None
        self.pause = False
        self.game_over = False

        self.score = 0
        self.level = 0
        self.total_lines = 0

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

    def create_block(self) -> Shape:
        # get random shape from all possible shapes
        block = self.shapes_list[random.randint(0, len(self.shapes_list) - 1)]()
        # calculate it's position - top center of the grid
        col = math.floor(self.grid.cols / 2) - math.ceil(len(block.shape) / 2)
        block.set_pos(Position(0, col))
        # randomly rotate the piece
        block.rotate(random.randint(0, 3))
        return block

    def load_next_blocks(self):
        if self.next_block is None:
            self.next_block = self.create_block()

        self.current_block = self.next_block
        self.set_block()
        self.next_block = self.create_block()

    def collides(self):
        # set the future position of the block
        # and check if there is already a piece on the grid there
        # along with that check if the block is not off the limits of the grid
        pos = self.current_block.position
        for row in range(self.current_block.rows):
            for col in range(self.current_block.cols):
                if self.current_block.shape[row][col] != 0:
                    if pos.col + col < 0 or pos.col + col > self.grid.last_col:
                        return True
                    if pos.row + row > self.grid.last_row:
                        return True
                    if self.grid[pos.row + row, pos.col + col] != 0:
                        return True
        return False

    def move_down(self):
        if not self.current_block or self.pause:
            return False

        self.remove_block()
        self.current_block.move_down()

        if self.collides():
            self.current_block.move_up()
            self.set_block()
            return False

        self.set_block()
        self.score += 1
        return True

    def move_bottom(self):
        while self.move_down():
            pass
        self.run(delay=False)

    def move_left(self, times=1):
        if not self.current_block or self.pause:
            return

        self.remove_block()
        self.current_block.move_left(times)
        if self.collides():
            self.current_block.move_right(times)
        self.set_block()

    def move_right(self, times=1):
        if not self.current_block or self.pause:
            return

        self.remove_block()
        self.current_block.move_right(times)
        if self.collides():
            self.current_block.move_left(times)
        self.set_block()

    def rotate(self):
        if not self.current_block or self.pause:
            return

        self.remove_block()
        self.current_block.rotate()

        # fix cases where block can't rotate if all the way to the left or right

        # if block is next to left wall move to the right and then rotate
        if self.collides() and self.current_block.position.col <= 0:
            for i in range(self.current_block.cols):
                self.current_block.move_right()
                if not self.collides():
                    break

        # if block is next to right wall move to the left and then rotate
        if self.collides() and (self.current_block.position.col + self.current_block.cols) >= self.grid.last_col:
            for i in range(self.current_block.cols):
                self.current_block.move_left()
                if not self.collides():
                    break

        if self.collides():
            # rotating 3 times returns it to it's original position
            self.current_block.rotate(3)
        self.set_block()

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

    def get_holes(self):
        holes = 0

        for row in transpose(self.grid.grid):
            for idx, el in enumerate(row):
                if el != 0:
                    holes += row[idx + 1:].count(0)
                    break
        return holes

    def get_bumpines(self):
        total_bumpiness = 0
        max_bumpiness = 0
        t_grid = transpose(self.grid.grid)
        cols_ids = []
        for col in t_grid:
            cols_ids.append(next((i for i, x in enumerate(col) if x), self.grid.rows))

        for i, idx in enumerate(cols_ids):
            try:
                bumpiness = abs(idx - cols_ids[i + 1])
                max_bumpiness = max(bumpiness, max_bumpiness)
                total_bumpiness += bumpiness
            except (TypeError, IndexError) as e:
                pass

        return total_bumpiness, max_bumpiness


    def get_height(self):
        sum_height = 0
        for col in transpose(self.grid.grid):
            sum_height += len(list(dropwhile(lambda x: x == 0, col)))
        return sum_height

    def get_state(self):
        holes = self.get_holes()
        total_bumpiness, max_bumpiness = self.get_bumpines()
        line_height = self.get_height()
        return [self.total_lines, holes, total_bumpiness, line_height]
