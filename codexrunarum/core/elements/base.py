from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from termcolor import colored


class BaseElement(ABC):
    @classmethod
    def compute_path(
        cls, movement_vector: np.ndarray[np.float32]
    ) -> np.ndarray[np.int8]:
        path = []
        current_point = np.array((0.0, 0.0))
        delta = movement_vector - current_point

        n = int(np.max(np.abs(delta)))

        if n == 0:
            return path

        dt = n
        dxdt = delta[1] / dt
        dydt = delta[0] / dt
        for _ in range(n):
            new_point = current_point + (dydt, dxdt)
            path.append(new_point.round() - current_point.round())
            current_point = new_point

        return np.array(path, dtype=np.int8)

    def to_string(self, colorcode: str | None = None):
        if colorcode is None:
            return self.__class__.__name__[0]

        return colored("●", colorcode)

    @abstractmethod
    def damage(self, amount: float):
        raise NotImplementedError

    @property
    @abstractmethod
    def power(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def propose_state(
        self, neighbors: np.ndarray[BaseElement | None]
    ) -> np.ndarray[BaseElement | None]:
        raise NotImplementedError

    @abstractmethod
    def merge(self, element: BaseElement):
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__class__.__name__[:5]
