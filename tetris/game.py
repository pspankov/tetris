import time


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

    def __init__(self, grid, delay=True):
        self.grid = grid

        self.pause = False
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

    def step(self):
        if not self.pause and not self.game_over:
            if self.grid.block.can_move:
                self.grid.move(0, 1)
            else:
                self.clear_complete_rows()
                if not self.is_game_over():
                    self.grid.create_block()

    """ Game options """

    def play_pause(self):
        if not self.game_over:
            self.pause = not self.pause
        else:
            self.reset_game()

    def reset_game(self):
        self.grid.reset()
        self.pause = False
        self.game_over = False

        self.score = 0
        self.level = 0
        self.lines = 0

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
        if not self.grid.block.can_move and self.grid.block.row <= 0:
            self.game_over = True
        return self.game_over

    def move_left(self):
        if not self.game_over and not self.pause:
            return self.grid.move(-1, 0)

    def move_right(self):
        if not self.game_over and not self.pause:
            return self.grid.move(1, 0)

    def move_down(self):
        if not self.game_over and not self.pause:
            moved = self.grid.move(0, 1)
            if moved:
                self.score += 1
            return moved

    def rotate(self):
        if not self.game_over and not self.pause:
            self.grid.rotate()

    def drop(self, check_state=True):
        """ Drop block all way down """
        while self.move_down():
            pass
        if check_state:
            self.clear_complete_rows()
            if not self.is_game_over():
                self.grid.create_block()
