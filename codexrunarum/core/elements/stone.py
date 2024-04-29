from __future__ import annotations

import numpy as np

from codexrunarum.core.elements.base import BaseElement


class Stone(BaseElement):
    id = 2

    def __init__(self, hardness: float):
        self._hardness = hardness

    @property
    def power(self) -> float:
        return self._hardness

    def propose_state(
        self, neighbors: np.ndarray[BaseElement | None]
    ) -> np.ndarray[BaseElement | None]:
        # stone is smart, stone doesnt move, doesnt evolve, doesnt degrate, be like stone
        propose = np.full_like(neighbors, None)
        propose[1, 1] = self
        return propose

    def merge(self, element: Stone):
        # how the hell you moved stone into another stone???
        self._hardness += element._hardness
