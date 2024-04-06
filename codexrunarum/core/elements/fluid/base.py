from abc import ABC, abstractmethod

from codexrunarum.core.elements.base import BaseElement


class BaseFluid(BaseElement, ABC):
    @property
    @abstractmethod
    def density(self) -> float:
        raise NotImplementedError
