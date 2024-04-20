from codexrunarum.core.elements.fluid.base import BaseFluid


class Water(BaseFluid):
    __id__ = 0
    __density__ = 0.99

    @property
    def density(self) -> float:
        return self.__density__

    @staticmethod
    def id(cls) -> int:
        return cls.__id__
