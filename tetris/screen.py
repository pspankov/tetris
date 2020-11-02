import turtle
from . import Position, Grid, Colors
from .tetris import Tetris


class Screen:
    STAMP_SIZE = 20

    def __init__(self, grid: Grid, tetris: Tetris, block_size=20):
        self.grid = grid
        self.tetris = tetris
        self.block_size = block_size
        self.grid_width = self.grid.cols * self.block_size
        self.grid_height = self.grid.rows * self.block_size

        self.width = self.grid_width * 2 + self.block_size * 2
        self.height = self.grid_height + self.block_size * 2

        self.s = self.init_screen()
        self.t = self.create_square_pen()
        self.score_pen = self.create_pen()
        self.static_pen = self.create_pen()

    def init_screen(self):
        s = turtle.getscreen()
        s.title('TETR1S by Pavel')
        s.bgcolor('black')
        s.setup(width=self.width, height=self.height)
        s.tracer(0)

        s.onkeypress(self.tetris.play_pause, 'p')
        s.onkeypress(self.tetris.reset_game, 'r')
        s.onkeypress(self.tetris.move_left, 'a')
        s.onkeypress(self.tetris.move_right, 'd')
        s.onkeypress(self.tetris.rotate, 'w')
        s.onkeypress(self.tetris.move_down, 's')
        s.onkeypress(self.tetris.move_bottom, 'space')
        s.listen()

        return s

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

    def clear(self):
        self.t.clear()

    def draw_score(self):
        self.score_pen.clear()
        self.score_pen.color('white')
        self.score_pen.goto(self.block_size, self.height/2 - self.block_size*4)
        self.score_pen.write(f'Score: {self.tetris.score} \nLines: {self.tetris.total_lines}',
                             font=('Arial', 18, 'normal'))
        self.score_pen.up()

    def draw_border(self):
        top_left = Position(self.height/2 - self.block_size, -self.width/2 + self.block_size)
        self.static_pen.up()
        self.static_pen.home()
        self.static_pen.color('gray')
        self.static_pen.goto(top_left.col, top_left.row)
        self.static_pen.down()
        self.static_pen.fd(self.grid_width)
        self.static_pen.right(90)
        self.static_pen.fd(self.grid_height)
        self.static_pen.right(90)
        self.static_pen.fd(self.grid_width)
        self.static_pen.right(90)
        self.static_pen.fd(self.grid_height)
        self.static_pen.up()

    def draw_info(self):
        self.static_pen.color('white')
        self.static_pen.goto(0 + self.block_size, -self.height / 4)
        info = 'Key commands: \r\n' \
               '<P> play/pause \n' \
               '<R> reset game \n' \
               '<A> move left \n' \
               '<D> move right \n' \
               '<W> rotate \n' \
               '<S> move down \n' \
               '<SPACE> move bottom'
        self.static_pen.write(info, font=('Arial', 10, 'normal'))
        self.static_pen.up()

    def draw_game_over(self):
        self.t.color('white')
        self.t.goto(-self.width/4 - self.block_size, 0)
        self.t.write('GAME OVER', font=('Arial', 10, 'normal'))
        self.t.up()

    def draw_grid(self):
        # top_left = Position(self.grid_height/2 - self.block_size/2, -self.grid_width/2 + self.block_size/2)
        row = self.height/2 - self.block_size - self.block_size/2
        col = -self.width/2 + self.block_size + self.block_size/2
        top_left = Position(row, col)

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                screen_x = top_left.col + (col * 20)
                screen_y = top_left.row - (row * 20)
                self.t.color(Colors(self.grid[row, col]).name)
                self.t.up()
                self.t.goto(screen_x, screen_y)
                self.t.down()
                self.t.stamp()
                self.t.up()

    def mainloop(self):
        while True:
            if self.tetris.game_over:
                self.clear()
                self.draw_game_over()
            else:
                # self.s.update()
                self.clear()
                self.draw_grid()
                self.draw_border()
                self.draw_info()
                self.draw_score()
