from codexrunarum.core.elements.spread.base import BaseSpread


class Fire(BaseSpread):
    __id__ = 2
    __dispersal__ = 0.3

    @property
    def dispersal(self):
        return self.__dispersal__

    @staticmethod
    def id(cls) -> int:
        return cls.__id__
