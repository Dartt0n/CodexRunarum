from __future__ import annotations

import random

import numpy as np
from icecream import ic

from .base import BaseElement
from .tree import Tree


class Fire(BaseElement):
    id = 1

    def __init__(self, temperature: float, direction: np.ndarray[float]):
        self._temperature = temperature
        self._direction = direction
        self._path = BaseElement.compute_path(direction)

        self._decay = 0.1
        self._min_sustain = 0.1

    @property
    def power(self) -> float:
        return self._temperature

    def damage(self, amount: float):
        self._temperature -= amount

    def propose_state(self, neighbors: np.ndarray[None]) -> np.ndarray[None]:
        this = (1, 1)

        self._temperature -= self._decay

        propose = np.full_like(neighbors, None)
        propose[this] = self

        if self._temperature < self._min_sustain or len(self._path) == 0:
            propose[this] = None  # burn out
            return propose

        move, self._path = self._path[0], self._path[1:]
        self._direction -= move
        step = tuple(move + this)

        for r in range(3):
            for c in range(3):
                if isinstance(neighbors[r, c], Tree):
                    propose[r, c] = Fire(1, self._direction)

        dr = move[0]
        dc = move[1]

        if neighbors[step] is not None and not isinstance(neighbors[step], Fire):
            # new_element = Fire(self._temperature * 0.5, self._direction)
            # propose[step] = new_element

            if dr == 0 and dc != 0:
                new_moves = np.array([(1, dc), (-1, dc)])
            elif dc == 0 and dr != 0:
                new_moves = np.array([(dr, 1), (dr, -1)])
            else:
                new_moves = np.array([(dr, 0), (0, dc)])

            new_steps = []
            for new_move in new_moves:
                new_steps.append(tuple(new_move + this))
        else:
            new_steps = [step]

        for step in new_steps:
            if neighbors[step] is None:
                propose[this] = None
                propose[step] = self
                break
            elif isinstance(propose[step], Fire):
                propose[this] = None
                propose[step].merge(self)
                break

        if np.random.random() < (np.tanh(self._temperature / 10 + 1) + 1) / 2:
            flame_spread = random.choice(self.__flame_direction(dr, dc))
            flame_coord = tuple(move + flame_spread)
            new_element = Fire(
                self._temperature * 0.5, self.__flame_vector(flame_spread)
            )
            if isinstance(propose[flame_coord], Fire):
                propose[flame_coord].merge(new_element)
            else:
                propose[flame_coord] = new_element

        return propose

    def merge(self, element: Fire):
        self._temperature += element._temperature
        self._temperature = max(self._temperature, 10)

    def __flame_direction(self, dr, dc):
        if dr == 0 and dc != 0:
            return [(-1, 0), (1, 0), (-1, dc), (0, dc), (1, dc)]

        if dc == 0 and dr != 0:
            return [(0, -1), (0, 1), (dr, -1), (dr, 0), (dr, 1)]

        if dr != 0 and dc != 0:
            return [(dr, dc), (dr, 0), (0, dc), (dr, -1), (-1, dc)]

        return [(0, 0)]

    def __flame_vector(self, direction):
        direction = np.array(direction, dtype=np.float64)
        direction /= np.linalg.norm(direction)
        norm = np.linalg.norm(self._direction) / 2
        direction *= norm

        angle = np.random.uniform(-np.pi / 6, np.pi / 6)
        rotation_matrix = np.array(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        )
        return np.dot(rotation_matrix, direction).astype(np.int64)
