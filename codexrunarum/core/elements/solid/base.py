from abc import ABC

import numpy as np

from codexrunarum.core.elements.base import BaseElement


class BaseSolid(BaseElement, ABC):
    def __init__(self, energy: float):
        super().__init__(energy, np.array((0, 0)))

    def evolute(self, row: int, column: int) -> list[tuple[int, int, BaseElement]]:
        return [(row, column, self)]
