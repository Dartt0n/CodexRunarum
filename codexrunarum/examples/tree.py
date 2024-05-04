import numpy as np

from codexrunarum.core import elements
from codexrunarum.core.engine import Engine
from codexrunarum.examples.base import DemoBase


class Tree(DemoBase):

    def engine_init(self):
        self.engine = Engine(self.grid_rows, self.grid_cols)

        offset = self.grid_cols // 8

        for i in range(5):
            self.engine.spawn_element_at(
                self.grid_rows // 4 * 3 - 1,
                offset + (self.grid_cols - offset) // 5 * i,
                elements.Water(2, np.array((0, 0)), 0.0),
            )

            self.engine.spawn_element_at(
                self.grid_rows // 4 * 3 - 2,
                offset + (self.grid_cols - offset) // 5 * i,
                elements.Tree(3, np.array((-1, 0), None)),
            )

        self.engine_calls = 0

    def engine_call(self):
        if self.engine_calls % 200 == 0:
            self.engine_init()
        self.engine_calls += 1

        self.engine.evolute()
        grid = self.engine.grid_ids()
        return grid


game = Tree((1920, 1080), (80, 45))
game.run()
