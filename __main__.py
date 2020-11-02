import sys
import threading
from tetris import Grid
from tetris.screen import Screen
from tetris.tetris import Tetris

grid = Grid(22, 10)
tetris = Tetris(grid)
screen = Screen(grid, tetris)

x = threading.Thread(target=tetris.mainloop, daemon=True)
x.start()

screen.mainloop()

sys.exit('Game over ;(')
#screen.s.mainloop()
