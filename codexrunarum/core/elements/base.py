from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from termcolor import colored


class BaseElement(ABC):
    _energy: float
    _velocity: np.ndarray[np.float32]
    _path: np.ndarray[np.int8]

    def __init__(self, energy: float, velocity: np.ndarray[np.float32]):
        self._energy = energy
        self._velocity = velocity
        self._path = self.compute_path(self.velocity)

    def compute_path(self, velocity: np.ndarray[np.float32]) -> np.ndarray[np.int8]:
        path = []
        current_point = np.array((0.0, 0.0))
        delta = velocity - current_point

        n = int(np.max(np.abs(delta)))
        dt = n
        dxdt = delta[1] / dt
        dydt = delta[0] / dt
        for _ in range(n):
            new_point = current_point + (dydt, dxdt)
            path.append(new_point.round() - current_point.round())
            current_point = new_point

        return np.array(path, dtype=np.int8)

    @staticmethod
    @abstractmethod
    def id(cls) -> int:
        raise NotImplementedError

    @property
    def energy(self) -> float:
        return self._energy

    @property
    def velocity(self) -> np.ndarray[np.float32]:
        return self._velocity

    @abstractmethod
    def evolute(self, row: int, col: int) -> list[tuple[int, int, BaseElement]]:
        raise NotImplementedError

    def to_string(self, colorcode: str | None = None):
        if colorcode is None:
            return str(self.id)

        return colored("●", colorcode)
