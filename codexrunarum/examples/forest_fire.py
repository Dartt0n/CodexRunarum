import numpy as np

from codexrunarum.core import elements
from codexrunarum.core.engine import Engine
from codexrunarum.examples.base import DemoBase


class ForestFire(DemoBase):
    def engine_init(self):
        self.engine = Engine(self.grid_rows, self.grid_cols)

        for _ in range(int(self.grid_rows * self.grid_cols * 0.01)):
            r = np.random.randint(self.grid_rows)
            c = np.random.randint(self.grid_cols)

            self.engine.spawn_element_at(r, c, elements.Water(2, np.array((0, 0)), 0.0))

        for _ in range(int(self.grid_rows * self.grid_cols * 0.1)):
            r = np.random.randint(self.grid_rows)
            c = np.random.randint(self.grid_cols)
            self.engine.spawn_element_at(r, c, elements.Tree(3, np.array((0, 1), None)))

        self.engine_calls = 0

    def engine_call(self):
        if self.engine_calls % 200 == 0:
            self.engine_init()
        self.engine_calls += 1

        self.engine.spawn_element_at(
            self.grid_rows // 2,
            self.grid_cols - 1,
            elements.Fire(1, np.array((0, -self.grid_cols // 2))),
        )

        self.engine.evolute()
        grid = self.engine.grid_ids()
        return grid


game = ForestFire((800, 600), (800 // 16, 600 // 16))
game.run()
