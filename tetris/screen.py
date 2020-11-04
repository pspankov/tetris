import turtle
from tetris import Position, Grid, Colors
from tetris.game import Tetris


class Screen:
    STAMP_SIZE = 20
    BACKGROUND_COLOR = 'white'
    TEXT_COLOR = 'black'
    MIN_SCREEN_WIDTH = 420
    MIN_SCREEN_HEIGHT = 480

    def __init__(self, grid: Grid, tetris: Tetris, block_size=20):
        self.grid = grid
        self.tetris = tetris
        self.block_size = block_size
        self.grid_width = self.grid.cols * self.block_size
        self.grid_height = self.grid.rows * self.block_size

        self.width = self.grid_width * 2 + self.block_size * 2
        self.height = self.grid_height + self.block_size * 2
        self.width = self.width if self.width >= self.MIN_SCREEN_WIDTH else self.MIN_SCREEN_WIDTH
        self.height = self.height if self.height >= self.MIN_SCREEN_HEIGHT else self.MIN_SCREEN_HEIGHT

        self._quit = False

        self.s = self.init_screen()
        self.t = self.create_square_pen()
        self.score_pen = self.create_pen()
        self.static_pen = self.create_pen()

    def init_screen(self):
        s = turtle.Screen()
        s.title('TETR1S by Pavel')
        s.bgcolor(self.BACKGROUND_COLOR)
        s.setup(width=self.width, height=self.height)
        s.tracer(0)

        s.onkeypress(self.tetris.play_pause, 'p')
        s.onkeypress(self.tetris.reset_game, 'r')
        s.onkeypress(self.tetris.move_left, 'a')
        s.onkeypress(self.tetris.move_right, 'd')
        s.onkeypress(self.tetris.rotate, 'w')
        s.onkeypress(self.tetris.move_down, 's')
        s.onkeypress(self.tetris.move_bottom, 'space')
        s.onkeypress(self.quit, 'q')
        s.listen()

        return s

    def mainloop(self):
        self.static_pen.clear()
        self.draw_border()
        self.draw_info()

        while not self._quit:
            if self.tetris.game_over:
                self.draw_game_over()
            else:
                # self.s.update()
                self.draw_grid()
                self.draw_next_block()
                self.draw_score()

        self.s.bye()

    def create_pen(self):
        t = turtle.Turtle()
        t.hideturtle()
        t.up()
        t.speed(0)
        t.setundobuffer(1)
        return t

    def create_square_pen(self):
        t = self.create_pen()
        t.shape('square')
        t.resizemode('user')
        t.shapesize(self.block_size / self.STAMP_SIZE)
        return t

    def quit(self):
        self.tetris.quit = True
        self._quit = True

    def draw_grid(self):
        self.t.clear()
        row = self.height / 2 - self.block_size - self.block_size / 2
        col = -self.width / 2 + self.block_size + self.block_size / 2
        top_left = Position(row, col)

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                screen_x = top_left.col + (col * self.block_size)
                screen_y = top_left.row - (row * self.block_size)
                if self.grid[row, col] != Colors.BACKGROUND.value:
                    self.t.color(Colors(self.grid[row, col]).name)
                else:
                    self.t.color(self.BACKGROUND_COLOR)
                self.t.goto(screen_x, screen_y)
                self.t.stamp()

    def draw_score(self):
        self.t.color(self.TEXT_COLOR)
        self.t.goto(self.block_size, self.block_size * 4)
        self.t.write(f'Score: {self.tetris.score} \nLines: {self.tetris.total_lines}',
                     font=('', 18, 'normal'))

    def draw_border(self):
        top_left = Position(self.height / 2 - self.block_size + 1, -self.width / 2 + self.block_size - 1)
        self.static_pen.color('gray')
        self.static_pen.goto(top_left.col, top_left.row)
        self.static_pen.down()
        self.static_pen.fd(self.grid_width + 2)
        self.static_pen.right(90)
        self.static_pen.fd(self.grid_height + 2)
        self.static_pen.right(90)
        self.static_pen.fd(self.grid_width + 2)
        self.static_pen.right(90)
        self.static_pen.fd(self.grid_height + 2)
        self.static_pen.up()

    def draw_info(self):
        self.static_pen.color(self.TEXT_COLOR)
        self.static_pen.goto(0 + self.block_size, -self.height / 2 + 20)
        info = 'Key commands: \r\n' \
               '<P> play/pause \n' \
               '<R> reset game \n' \
               '<A> move left \n' \
               '<D> move right \n' \
               '<W> rotate \n' \
               '<S> move down \n' \
               '<SPACE> move bottom \n' \
               '<Q> quit'
        self.static_pen.write(info, font=('', 11, 'normal'))
        self.static_pen.up()

    def draw_next_block(self):
        if not self.tetris.next_block:
            return

        top_left = Position(self.height / 2 - self.block_size * 2, self.block_size * 2)

        for row in range(self.tetris.next_block.rows):
            for col in range(self.tetris.next_block.cols):
                screen_x = top_left.col + (col * self.block_size)
                screen_y = top_left.row - (row * self.block_size)
                if self.tetris.next_block.shape[row][col] != Colors.BACKGROUND.value:
                    self.t.color(Colors(self.tetris.next_block.shape[row][col]).name)
                else:
                    self.t.color(self.BACKGROUND_COLOR)
                self.t.goto(screen_x, screen_y)
                self.t.stamp()

    def draw_game_over(self):
        self.t.color(self.TEXT_COLOR)
        self.t.goto(-self.width / 4 - self.block_size, 0)
        self.t.write('GAME OVER', font=('', 10, 'normal'))
        self.t.up()
