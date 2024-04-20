import numpy as np

from codexrunarum.core.elements.solid.base import BaseSolid


class Tree(BaseSolid):
    __id__ = 5
    _grow_coef = 0.3
    _withering = 0.3

    @classmethod
    def id(cls) -> int:
        return cls.__id__

    @property
    def grow_coef(self):
        return self._grow_coef

    @property
    def withering(self):
        return self._withering

    def evolute(self, row: int, column: int) -> list[tuple[int, int, BaseSolid]]:
        self._energy -= self.withering
        if self.energy < 0:
            if -1 / self.energy < np.random.random():
                return []
            else:
                return [(row, column, self)]

        new_elements = []
        new_elements.append((row, column, self))
        grow_dir = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ][np.random.choice(8)]
        newTree = Tree(self.energy * self.grow_coef)
        new_elements.append(
            (
                row + grow_dir[0],
                column + grow_dir[1],
                newTree,
            )
        )
        self._energy = self.energy * (1 - self.grow_coef)
        return new_elements
