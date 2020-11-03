# Tetris

### Run without installation
```bash
$ python3 /<path-to-cloned-project/tetris
```

### Installation
```bash
$ pip install /<path-to-cloned-project/
```

Run the game in the console
```bash
$ tetris
```

### Example usage
```python
import threading
from tetris import Grid
from tetris.screen import Screen
from tetris.game import Tetris


def main():
    # create the tetris grid
    grid = Grid(22, 10)
    
    # initialize the game
    tetris = Tetris(grid)
    
    # the screen implementation can be replaced with
    # other visualisation class if needed
    screen = Screen(grid, tetris)
    
    # start the tetris thread (it needs it's own delay independent of the screen rendering)
    x = threading.Thread(target=tetris.mainloop, name='tetris')
    x.start()
    
    # start the screen loop
    screen.mainloop()
    x.join()
    print('Bye!')


if __name__ == '__main__':
    main()
```