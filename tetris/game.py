import time
import math
from .blocks import Bag
from .grid import Grid, Collision


class Tetris:
    """ Tetris mechanics
        https://meatfighter.com/nintendotetrisai/#The_Mechanics_of_Nintendo_Tetris
    """

    '''
    Lines cleared   Points
        0           0
        1           40
        2           100
        3           300
        4           1200 '''
    POINTS = [0, 40, 100, 300, 1200]
    # Game speed for levels from 0 to 9
    GAME_SPEED = [.799, .715, .632, .549, .466, .383, .300, .216, .133, .100]

    def __init__(self, grid: Grid, bag: Bag, delay=True):
        self.grid = grid
        self.bag = bag

        self.block = None
        self.next_block = None

        self.running = False
        self.pause = True
        self.game_over = False
        self.quit = False

        self.score = 0
        self.level = 0
        self.lines = 0

        self.delay = delay

    def get_game_speed(self):
        if not self.delay:
            return 0

        try:
            return self.GAME_SPEED[self.level]
        except IndexError:
            pass
        if 10 >= self.level <= 12:
            return .083
        elif 13 >= self.level <= 15:
            return .067
        elif 16 >= self.level <= 18:
            return .050
        elif 19 >= self.level <= 28:
            return .033
        elif self.level >= 29:
            return .017

    def mainloop(self, delay=True):
        while not self.quit:
            self.step()
            if delay:
                time.sleep(self.get_game_speed())

    # GAME OPTIONS
    def start_game(self):
        if not self.running:
            self.create_block()
            self.running = True
            self.play_pause()

    def play_pause(self):
        if not self.game_over and self.running:
            self.pause = not self.pause

    def reset_game(self):
        self.grid.reset()
        self.bag.empty()
        self.pause = True
        self.running = False
        self.game_over = False

        self.score = 0
        self.level = 0
        self.lines = 0

    # GAME LOGIC

    def step(self):
        if not self.pause and not self.game_over:
            if self.block.can_move:
                self.move(0, 1)
            else:
                self.clear_complete_rows()
                if not self.is_game_over():
                    self.create_block()

    def create_block(self):
        if not self.bag.blocks:
            self.bag.fill()

        if self.next_block is None:
            self.block = self.bag.blocks.pop()
        else:
            self.block = self.next_block

        # calculate it's position - top center of the grid
        col = math.floor(self.grid.cols / 2) - math.ceil(self.block.width / 2)
        self.block.col = col
        self.next_block = self.bag.blocks.pop()
        self.grid.set_block(self.block)

        return self.block

    def clear_complete_rows(self):
        # when row columns are filled we need the clear them out (the rules of the game :))
        rows_cleared = 0
        for row in range(self.grid.rows):
            if 0 not in self.grid[row]:
                rows_cleared += 1
                self.grid.delete_row(row)

        if rows_cleared > 0:
            self.lines += rows_cleared
            self.score += self.POINTS[rows_cleared] * (self.level + 1)
            lines_to_level_up = 10 * (self.level + 1)
            if self.lines >= lines_to_level_up:
                self.level += 1

        return rows_cleared

    def is_game_over(self):
        if not self.block.can_move and self.block.row <= 0:
            self.game_over = True
        return self.game_over

    # GAME MOVEMENT
    def move(self, col=0, row=0):
        if not self.block.can_move:
            return

        self.grid.remove_block(self.block)
        self.block.move(col, row)

        if self.grid.collides(self.block):
            self.block.move(-col, -row)
            self.grid.set_block(self.block)
            if col == 0:  # if it's moved down
                self.block.can_move = False
            return False
        else:
            self.grid.set_block(self.block)
            return True

    def move_left(self):
        if not self.game_over and not self.pause:
            return self.move(-1, 0)

    def move_right(self):
        if not self.game_over and not self.pause:
            return self.move(1, 0)

    def move_down(self):
        if not self.game_over and not self.pause:
            moved = self.move(0, 1)
            if moved:
                self.score += 1
            return moved

    def rotate(self):
        if not self.game_over and not self.pause:
            if not self.block.can_move:
                return

            self.grid.remove_block(self.block)
            self.block.rotate()

            # fix cases where block can't rotate if all the way to the left or right

            # if block is next to left wall move to the right and then rotate
            collision = self.grid.collides(self.block)
            if collision == Collision.LEFT_WALL:
                for i in range(self.block.width):
                    self.block.move(1, 0)
                    if not self.grid.collides(self.block):
                        break

            # if block is next to right wall move to the left and then rotate
            if collision == Collision.RIGHT_WALL:
                for i in range(self.block.width):
                    self.block.move(-1, 0)
                    if not self.grid.collides(self.block):
                        break

            if self.grid.collides(self.block):
                # rotating 3 times returns it to it's original position
                self.block.rotate(3)
                self.grid.set_block(self.block)
                return False

            self.grid.set_block(self.block)
            return True

    def drop(self, check_state=True):
        """ Drop block all way down """
        while self.move_down():
            pass
        if check_state:
            self.clear_complete_rows()
            if not self.is_game_over():
                self.create_block()
