import numpy as np

from codexrunarum.core import elements
from codexrunarum.core.engine import Engine
from codexrunarum.examples.base import DemoBase


class Water(DemoBase):
    def engine_init(self):
        self.engine = Engine(self.grid_rows, self.grid_cols)

        self.engine.spawn_element_at(
            self.grid_rows // 2, 0, elements.Water(25, np.array((0, 1)), 10.0)
        )

        self.engine_calls = 0

    def engine_call(self):
        if self.engine_calls % 25 == 0:
            self.engine_init()
        self.engine_calls += 1

        self.engine.evolute()
        grid = self.engine.grid_ids()
        return grid


game = Water((1920, 1080), (160, 90), 15)
game.run()
