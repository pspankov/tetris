import threading

from tetris.game import Tetris
from tetris.grid import Grid
from tetris.blocks import Bag
from tetris.screen import Screen


def main():
    # mini_shapes = [shapes.MiniBlock, shapes.MiniOne, shapes.MiniTwo, shapes.MiniDiagTwo, shapes.MiniThree]
    tetris = Tetris(Grid(20, 10), Bag())
    screen = Screen(tetris)

    x = threading.Thread(target=tetris.mainloop, name='Tetris')
    x.start()

    screen.mainloop()
    x.join(timeout=0)
    print('Bye!')


if __name__ == '__main__':
    main()
