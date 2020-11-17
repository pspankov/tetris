import threading

from tetris import Grid
from tetris.screen import Screen
from tetris.game import Tetris


def main():
    grid = Grid(20, 10)
    # mini_shapes = [shapes.MiniBlock, shapes.MiniOne, shapes.MiniTwo, shapes.MiniDiagTwo, shapes.MiniThree]
    tetris = Tetris(grid)
    screen = Screen(grid, tetris)

    x = threading.Thread(target=tetris.mainloop, name='Tetris')
    x.start()

    screen.mainloop()
    x.join(timeout=0)
    print('Bye!')


if __name__ == '__main__':
    main()
