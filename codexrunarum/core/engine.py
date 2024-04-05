import numpy as np
import numpy.typing as npt


class Engine:
    _grid_width: int
    _grid_height: int
    _grid: npt.NDArray[np.uint8]

    def __init__(self, grid_width: int, grid_height: int):
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._grid = np.empty((grid_height, grid_width), dtype=np.uint8)
