from __future__ import annotations

import random

import numpy as np
from icecream import ic

from codexrunarum.core.elements.base import BaseElement


class Water(BaseElement):
    id = 4

    def __init__(self, volume: float, direction: np.ndarray[float], momentum: float):
        self._volume = volume
        self._direction = direction
        self._momentum = momentum
        self._path = BaseElement.compute_path(direction * momentum)

        self._min_volume = 0.1
        self._momentum_decay = 0.1

    @property
    def power(self) -> float:
        return self._volume * (0.1 + self._momentum)

    def damage(self, amount: float):
        self._volume -= amount

    def propose_state(
        self, neighbors: np.ndarray[BaseElement | None]
    ) -> np.ndarray[BaseElement | None]:
        this = (1, 1)

        propose = np.full_like(neighbors, None)

        if self._volume > 0:
            propose[this] = self

        if self._momentum > 0 and len(self._path) > 0:
            move, self._path = self._path[0], self._path[1:]
            propose = self.__flow(neighbors, propose, move, this)
        elif self._volume > self._min_volume:
            propose = self.__spill(neighbors, propose, this)

        return propose

    def merge(self, element: Water):
        new_dir = (
            self._momentum * self._direction + element._momentum * element._direction
        )
        self._momentum = np.linalg.norm(new_dir)
        if self._momentum > 0:
            self._direction = new_dir / self._momentum
        else:
            self._direction = np.array((0, 0))
        self._volume += element._volume

    def __get_search_direction(self, dr, dc):
        if dr == 0 and dc != 0:
            stage0 = [(0, dc)]
            stage1 = [(-1, dc), (1, dc)]
            random.shuffle(stage1)
            stage2 = [(-1, 0), (1, 0)]
            random.shuffle(stage2)

            return stage0 + stage1 + stage2

        if dc == 0 and dr == 0:
            stage0 = [(dr, 0)]
            stage1 = [(dr, -1), (dr, 1)]
            random.shuffle(stage1)
            stage2 = [(0, 1), (0, -1)]
            random.shuffle(stage2)

            return stage0 + stage1 + stage2

        if dr != 0 and dc != 0:
            stage0 = [(dr, dc)]
            stage1 = [(dr, 0), (0, dc)]
            random.shuffle(stage1)
            stage2 = [(dr, -1), (-1, dc)]
            random.shuffle(stage2)

            return stage0 + stage1 + stage2

        return [(0, 0)]

    def __flow(self, neighbors, propose, move, this):
        step = tuple(move + this)
        dr = move[0]
        dc = move[1]
        self._momentum -= self._momentum_decay

        if neighbors[step] is not None and not isinstance(neighbors[step], Water):
            # there is an obstacle in the path, try find new direction
            new_directions = np.array(self.__get_search_direction(dr, dc))

            for direction in new_directions:
                new_step = tuple(this + direction)

                if neighbors[new_step] is None:
                    propose[this] = None
                    propose[new_step] = Water(
                        self._volume,
                        direction,
                        self._momentum - self._momentum_decay,
                    )
                    break

                if isinstance(neighbors[new_step], Water):
                    propose[this] = None
                    propose[new_step] = neighbors[new_step]
                    propose[new_step].merge(
                        Water(
                            self._volume,
                            direction,
                            self._momentum - self._momentum_decay,
                        )
                    )
                    break
            else:
                # can not find move forward, rotate
                backward_move = -move
                new_directions = np.array(
                    self.__get_search_direction(backward_move[0], backward_move[1])
                )
                for direction in new_directions:
                    new_step = tuple(this + direction)

                    if neighbors[new_step] is None:
                        propose[this] = None
                        propose[new_step] = Water(
                            self._volume,
                            direction,
                            self._momentum * 0.25,
                        )
                        break

                    if isinstance(neighbors[new_step], Water):
                        propose[this] = None
                        propose[new_step] = neighbors[new_step]
                        propose[new_step].merge(
                            Water(
                                self._volume,
                                direction,
                                self._momentum * 0.25,
                            )
                        )
                        break

        elif neighbors[step] is None:
            self._momentum -= self._momentum_decay
            propose[step] = self
            propose[this] = None
        elif isinstance(neighbors[step], Water):
            self._momentum -= self._momentum_decay
            propose[step] = neighbors[step]
            propose[step].merge(self)
            propose[this] = None

        return propose

    def __spill(self, neighbors, propose, this):
        directions = np.array([(-1, 0), (1, 0), (0, -1), (0, 1)])

        valid_steps = []

        for direction in directions:
            step = tuple(direction + this)

            if neighbors[step] is None:
                valid_steps.append(step)

        new_volume = self._volume / (len(valid_steps) + 1)

        if new_volume > self._min_volume:
            self._volume = new_volume
            self._momentum = 0
            self._direction = np.array([0, 0])
            propose[this] = self

            for step in valid_steps:
                propose[step] = Water(new_volume, self._direction, self._momentum)

        return propose
