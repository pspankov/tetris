import turtle
from tetris.grid import Grid
from tetris.game import Tetris


COLORS = ['#FFFFFF',  # background
          '#FFD500',  # Yellow O-block
          '#66A3ED',  # Lightblue I-block
          '#6B3ACF',  # Purple T-block
          '#0341AE',  # Blue J-block
          '#FF971C',  # Orange L-block
          '#FF3213',  # Red Z-block
          '#72CB3B']  # Green S-block


class Screen:
    STAMP_SIZE = 20
    TEXT_COLOR = 'black'
    MIN_SCREEN_WIDTH = 420
    MIN_SCREEN_HEIGHT = 420

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

        self.draw_border()
        self.draw_info()

    def init_screen(self):
        s = turtle.Screen()
        s.title('TETR1S by Pavel')
        s.bgcolor(COLORS[0])
        s.setup(width=self.width, height=self.height)
        s.tracer(0)

        s.onkeypress(self.tetris.play_pause, 'p')
        s.onkeypress(self.tetris.reset_game, 'r')
        s.onkeypress(self.tetris.move_left, 'a')
        s.onkeypress(self.tetris.move_right, 'd')
        s.onkeypress(self.tetris.rotate, 'w')
        s.onkeypress(self.tetris.move_down, 's')
        s.onkeypress(self.tetris.drop, 'space')
        s.onkeypress(self.quit, 'q')
        s.listen()

        return s

    def draw(self):
        self.s.update()

        # while not self._quit:
        self.t.clear()
        self.draw_grid()
        self.draw_next_block()
        self.draw_score()

        if self.tetris.game_over:
            self.draw_game_over()

        if self._quit:
            self.s.bye()

        self.s.ontimer(self.draw)

    def mainloop(self):
        self.draw()
        self.s.mainloop()

    def create_pen(self):
        t = turtle.Turtle()
        t.speed(0)
        t.hideturtle()
        t.up()
        t.setundobuffer(0)
        return t

    def create_square_pen(self):
        t = self.create_pen()
        t.shape('square')
        t.resizemode('user')
        t.shapesize(self.block_size / self.STAMP_SIZE)
        t.setundobuffer(0)
        return t

    def quit(self):
        self.tetris.quit = True
        self._quit = True

    def draw_grid(self):
        x = -self.width / 2 + self.block_size + self.block_size / 2
        y = self.height / 2 - self.block_size - self.block_size / 2

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                screen_x = x + (col * self.block_size)
                screen_y = y - (row * self.block_size)
                self.t.color(COLORS[self.grid[row, col]])
                self.t.goto(screen_x, screen_y)
                self.t.stamp()

    def draw_score(self):
        self.t.color(self.TEXT_COLOR)
        self.t.goto(self.block_size, self.block_size * 3)
        info = f'Score: {self.tetris.score} \nLines: {self.tetris.lines}\nLevel: {self.tetris.level}'
        self.t.write(info, font=('', 18, 'normal'), move=False)

    def draw_border(self):
        x = -self.width / 2 + self.block_size - 1
        y = self.height / 2 - self.block_size + 1

        self.static_pen.color('gray')
        self.static_pen.goto(x, y)
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
        self.static_pen.goto(0 + self.block_size, -self.height / 3)
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
        if not self.grid.next_block:
            return

        x = self.block_size * 2
        y = int(self.height / 2 - self.block_size * 2)

        for row in range(self.grid.next_block.height):
            for col in range(self.grid.next_block.width):
                screen_x = x + (col * self.block_size)
                screen_y = y - (row * self.block_size)
                self.t.color(COLORS[self.grid.next_block.shape[row][col]])
                self.t.goto(screen_x, screen_y)
                self.t.stamp()

    def draw_game_over(self):
        self.t.color(self.TEXT_COLOR)
        self.t.goto(-self.width / 4 - self.block_size*2, 0)
        self.t.write('GAME OVER', font=('', 16, 'normal'))
