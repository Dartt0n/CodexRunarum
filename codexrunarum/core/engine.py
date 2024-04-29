from itertools import product
from statistics import mean

import numpy as np
from icecream import ic

from codexrunarum.core.elements import BaseElement, Fire, Stone, Tree, Water


class Engine:
    _cols: int
    _rows: int
    _grid: np.ndarray[BaseElement | None]
    _freezed: np.ndarray[bool]
    _n_unchanged: np.ndarray[int]

    def __init__(self, rows: int, cols: int):
        self._state_idx = 0
        self._cols = cols
        self._rows = rows

        self._grid = np.full((rows, cols), None, dtype=object)

    def spawn_element_at(self, row: int, col: int, element: BaseElement):
        self._grid[row, col] = element

    def spawn_pattern(self, row: int, col: int, pattern: np.ndarray[BaseElement]):
        prows, pcols = pattern.shape[:2]

        self._grid[row : row + prows, col : col + pcols] = pattern

    def print_state(self, colormap: dict[int, str] | None = None, spacing: str = " "):
        if colormap is None:
            colormap = {}

        rows = (
            spacing.join(
                element.to_string(colormap.get(element.id)) if element else " "
                for element in row
            )
            for row in self._grid
        )

        print(
            *rows,
            sep="\n",
        )
        print("state", self._state_idx)
        mean_power = mean(0 if x is None else x.power for x in self._grid.flatten())
        print("mean power", mean_power)

    def evolute(self):
        next_state = np.full_like(self._grid, None)
        candidates = [[[] for c in range(self._cols)] for r in range(self._rows)]

        for row, col in self._itergrid():
            if self._grid[row, col] is None:
                continue

            current_element: BaseElement = self._grid[row, col]
            current_local_state = self._get_neighbors(row, col)
            next_local_state = current_element.propose_state(current_local_state)

            for r, c in self._itergrid(0, 3, 0, 3):
                prop_row = r + row - 1
                prop_col = c + col - 1
                prop_element = next_local_state[r, c]
                if 0 <= prop_row < self._rows and 0 <= prop_col < self._cols:
                    candidates[prop_row][prop_col].append(prop_element)

        for row, col in self._itergrid():
            next_state[row, col] = self._resolve_conflict(candidates[row][col])

        self._state_idx += 1
        self._grid = next_state

    def grid_ids(self) -> np.ndarray:
        ids = np.zeros((self._rows * self._cols,), dtype=np.uint8)
        for i, element in enumerate(self._grid.flatten()):
            ids[i] = element.id if element else 0
        return ids.reshape(self._grid.shape)

    def _shrink_valid(
        self, minr: int, maxr: int, minc: int, maxc: int
    ) -> tuple[int, int, int, int]:
        return (
            max(minr, 0),
            min(maxr, self._rows),
            max(minc, 0),
            min(maxc, self._cols),
        )

    def _itermesh(self, minr: int, maxr: int, minc: int, maxc: int):
        yield from product(range(minr, maxr), range(minc, maxc))

    def _itergrid(
        self,
        minr: int | None = None,
        maxr: int | None = None,
        minc: int | None = None,
        maxc: int | None = None,
    ):
        minr, maxr, minc, maxc = self._shrink_valid(
            minr or 0, maxr or self._rows, minc or 0, maxc or self._cols
        )
        yield from self._itermesh(minr, maxr, minc, maxc)

    def _grid_at(self, row: int, col: int) -> BaseElement | None:
        if self._rows <= row or row < 0:
            return None

        if self._cols <= col or col < 0:
            return None

        return self._grid[row, col]

    def _get_neighbors(self, row: int, col: int) -> np.ndarray[BaseElement | None]:
        neighbors = np.full((3, 3), None, dtype=object)
        for r, c in self._itermesh(0, +3, 0, +3):
            neighbors[r, c] = self._grid_at(row + r - 1, col + c - 1)
        return neighbors

    def _resolve_conflict(self, candidates: list[BaseElement]) -> BaseElement | None:
        candidates = list(filter(None, candidates))

        if len(candidates) == 0:
            return None

        if len(candidates) == 1:
            return candidates[0]

        elements = {}

        for candidate in candidates:
            if candidate.id not in elements:
                elements[candidate.id] = candidate
            else:
                elements[candidate.id].merge(candidate)

        if len(elements) == 1:
            return next(iter(elements.values()))

        if Stone.id in elements:
            if Water.id in elements:
                elements[Stone.id].damage(elements[Water.id].power)

            if Fire.id in elements:
                elements[Stone.id].damage(elements[Fire.id].power)

        if Water.id in elements and Fire.id in elements:
            diff = elements[Water.id].power - elements[Fire.id].power

            if diff > 0:
                elements[Water.id].damage(diff)
            else:
                elements[Fire.id].damage(-diff)

        if Tree.id in elements and Water.id in elements:
            elements[Water.id].damage(elements[Tree.id].power / 10)

        return max(elements.values(), key=lambda x: x.power)
