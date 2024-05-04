import numpy as np

from codexrunarum.core import elements
from codexrunarum.core.engine import Engine
from codexrunarum.examples.base import DemoBase


class Fire(DemoBase):
    def engine_init(self):
        self.engine = Engine(self.grid_cols, self.grid_rows)

        self.engine.spawn_element_at(
            self.grid_rows // 2,
            self.grid_cols // 2,
            elements.Fire(4, np.array((0, 50))),
        )

        self.engine_calls = 0

    def engine_call(self):
        if self.engine_calls % 20 == 0:
            self.engine_init()
        self.engine_calls += 1

        self.engine.evolute()
        grid = self.engine.grid_ids()
        return grid


game = Fire((1920, 1080), (80, 45))
game.run()
