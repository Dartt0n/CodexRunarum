from __future__ import annotations

import random

import numpy as np

from .base import BaseElement
from .water import Water


class Tree(BaseElement):
    id = 3

    def __init__(
        self,
        health: float,
        direction: np.ndarray[float],
        parent: Tree | None = None,
    ):
        self._health = health
        self._parent = parent
        self._withering = 0.2
        self._water_near = False
        self._direction = direction

    @property
    def power(self) -> float:
        return self._health

    @property
    def is_suplied(self) -> float:
        if self._water_near:
            return True

        if self._parent is None:
            return False

        return self._parent.is_suplied

    def merge(self, other: Tree):
        self._health = max(self._health, other._health)

    def damage(self, amount: float):
        self._health -= amount

    def propose_state(self, neighbors: np.ndarray[BaseElement | None]):
        propose = np.full_like(neighbors, None)
        this = (1, 1)
        propose[this] = self

        trees_amount = sum(1 if isinstance(e, Tree) else 0 for e in neighbors.flatten())

        self._water_near = False
        for element in neighbors.flatten():
            if isinstance(element, Water):
                self._water_near = True
                self._parent = None
                self._health = 3
                break

        suplied = self.is_suplied
        if not suplied:
            self._health -= self._withering * trees_amount
        else:
            self._health -= self._withering * (trees_amount / 2)

        if self._health < 0:
            propose[this] = None

        if not suplied:  # can not grow
            return propose

        if random.random() < 0.4:
            tries = 1
            new_node = self.__get_grow_direction(self._direction)
            step = (this[0] + new_node[0], this[1] + new_node[1])
            while isinstance(neighbors[step], Water) and tries < 5:
                new_node = self.__get_grow_direction(self._direction)
                step = (this[0] + new_node[0], this[1] + new_node[1])
                tries += 1

            propose[step] = Tree(self._health, self._direction, self)

        return propose

    def __get_grow_direction(self, direction):
        dr, dc = direction

        if dr == 0 and dc != 0:
            return random.choice([(-1, dc), (1, dc), (dr, dc)])

        if dc == 0 and dr != 0:
            return random.choice([(dr, -1), (dr, 1), (dr, dc)])

        return random.choice([(0, dc), (dr, 0), (dr, dc)])
