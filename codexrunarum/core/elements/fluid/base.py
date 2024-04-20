from abc import ABC, abstractmethod

import numpy as np

from codexrunarum.core.elements.base import BaseElement


class BaseFluid(BaseElement, ABC):
    @property
    @abstractmethod
    def density(self) -> float:
        raise NotImplementedError

    @property
    def energy(self) -> float:
        return self._energy
        # TODO: make decrease when moving

    def __init__(self, velocity, energy=None):
        if energy is None:
            super().__init__(energy=np.linalg.norm(velocity), velocity=velocity)
        else:
            super().__init__(energy=energy, velocity=velocity)

    def evolute(self, row: int, column: int) -> list[tuple[int, int, BaseElement]]:
        if len(self._path) == 0:
            return [(row, column, self)]

        if self.energy < 0.01:
            return []

        delta, self._path = self._path[0], self._path[1:]
        new_elements = []

        new_elements.append((row, column, self))
        self._velocity -= delta
        new_elements.append(
            (
                delta[0] + row,
                delta[1] + column,
                self.__class__(
                    velocity=self.velocity, energy=self.density * self.energy
                ),
            )
        )
        self._energy = (1 - self.density) * self._energy
        return new_elements
