from __future__ import annotations

import numpy as np

from codexrunarum.core.elements.base import BaseElement


class Stone(BaseElement):
    id = 2

    def __init__(self, hardness: float):
        self._hardness = hardness

    def damage(self, amount: float):
        self._hardness -= amount

    @property
    def power(self) -> float:
        return self._hardness

    def propose_state(
        self, neighbors: np.ndarray[BaseElement | None]
    ) -> np.ndarray[BaseElement | None]:
        propose = np.full_like(neighbors, None)
        if self._hardness > 0:
            propose[1, 1] = self
        return propose

    def merge(self, element: Stone):
        self._hardness += element._hardness
