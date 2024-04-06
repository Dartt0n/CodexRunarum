from __future__ import annotations

import numpy as np

from codexrunarum.core.elements.base import BaseElement


class Void(BaseElement):
    __id__ = 0

    @staticmethod
    def new() -> Void:
        return Void(0.0, np.array((0.0, 0.0)))

    @classmethod
    def id(cls) -> int:
        return cls.__id__

    def evolute(self, _row: int, _col: int) -> list[tuple[int, int, BaseElement]]:
        return []
