import numpy as np

from codexrunarum.core.elements.base import BaseElement
from codexrunarum.core.elements.void import Void

V = Void.new()


class Engine:
    _grid_width: int
    _grid_height: int
    _grid: np.ndarray[object]

    def __init__(self, grid_height: int, grid_width: int):
        self._state_idx = 0
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._grid = np.empty((grid_height, grid_width), dtype=object)
        self._grid[:, :] = V

    def spawn_element_at(self, row: int, col: int, element: BaseElement):
        self._grid[row, col] = element

    def get_at(self, row: int, col: int) -> BaseElement:
        return self._grid[row, col]

    def spawn_pattern(self, row: int, col: int, pattern: np.ndarray[BaseElement]):
        prows, pcols = pattern.shape[:2]
        self._grid[row : row + prows, col : col + pcols] = pattern

    def print_state(self, colormap: dict[int, str] | None = None, spacing: str = " "):
        if colormap is None:
            colormap = {}

        rows = (
            spacing.join(element.to_string(colormap.get(element.id)) for element in row)
            for row in self._grid
        )

        print(
            *rows,
            sep="\n",
        )
        print("state", self._state_idx)

    def evolute(self):
        next_state = np.empty_like(self._grid)
        next_state[:, :] = V

        for row in range(self._grid_height):
            for col in range(self._grid_width):
                new_elements = self._grid[row, col].evolute(row, col)
                for new_row, new_col, new_element in new_elements:
                    if (
                        0 <= new_row < self._grid_height
                        and 0 <= new_col < self._grid_width
                        and next_state[new_row, new_col].id == V.id
                    ):
                        next_state[new_row, new_col] = new_element

        self._state_idx += 1
        self._grid = next_state
