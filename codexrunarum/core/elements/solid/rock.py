from codexrunarum.core.elements.solid.base import BaseSolid


class Rock(BaseSolid):
    __id__ = 1

    @classmethod
    def id(cls) -> int:
        return cls.__id__
