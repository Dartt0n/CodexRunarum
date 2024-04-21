from abc import ABC, abstractmethod

import numpy as np

from codexrunarum.core.elements.base import BaseElement


class BaseSpread(BaseElement, ABC):
    def __init__(self, velocity: np.ndarray[np.float32]):
        super().__init__(energy=0.0, velocity=velocity)

    @property
    def energy(self) -> float:
        return np.linalg.norm(self.velocity)

    @property
    @abstractmethod
    def dispersal(self) -> float:
        raise NotImplementedError

    def evolute(self, row: int, col: int) -> list[tuple[int, int, BaseElement]]:
        new_elements = []
        if self.energy == 0:
            # energy of this element is decreased to zero and therefore
            # it can not continue existing any more
            return new_elements

        if len(self._path) == 0:
            # if path is ended, stay in place
            return [(row, col, self)]

        delta, self._path = self._path[0], self._path[1:]
        new_row, new_col = delta + (row, col)
        new_elements.append((new_row, new_col, self))
        self._velocity -= delta

        if np.random.random() > self.dispersal:
            # fail to spread
            return new_elements

        if delta[0] == 0 and delta[1] != 0:
            new_elements.append(
                (new_row - 1, new_col, self.__class__(velocity=self._velocity.copy()))
            )
            new_elements.append(
                (new_row + 1, new_col, self.__class__(velocity=self._velocity.copy()))
            )
        elif delta[1] == 0 and delta[0] != 0:
            new_elements.append(
                (new_row, new_col - 1, self.__class__(velocity=self._velocity.copy()))
            )
            new_elements.append(
                (new_row, new_col + 1, self.__class__(velocity=self._velocity.copy()))
            )
        else:
            new_elements.append(
                (
                    new_row,
                    new_col + delta[1],
                    self.__class__.__init__(velocity=self._velocity.copy()),
                )
            )
            new_elements.append(
                (
                    new_row + delta[0],
                    new_col,
                    self.__class__.__init__(velocity=self._velocity.copy()),
                )
            )

        return new_elements
