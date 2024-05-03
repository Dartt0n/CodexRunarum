import numpy as np

from codexrunarum.core import elements
from codexrunarum.core.engine import Engine
from codexrunarum.examples.base import DemoBase


class FireClock(DemoBase):
    def engine_init(self):
        self.engine = Engine(self.grid_rows, self.grid_cols)

        self.engine_calls = 0
        self.direction = 0

    def engine_call(self):
        DIRECTIONS = [
            np.array((0, 100)),
            np.array((100, 100)),
            np.array((100, 0)),
            np.array((100, -100)),
            np.array((0, -100)),
            np.array((-100, -100)),
            np.array((-100, 0)),
            np.array((-100, 100)),
        ]

        if self.engine_calls % 50 == 0:
            self.engine.spawn_element_at(
                self.grid_rows // 2,
                self.grid_cols // 2,
                elements.Fire(3, DIRECTIONS[self.direction % 8]),
            )
            self.engine_calls = 0
            self.direction += 1

        self.engine_calls += 1
        self.engine.evolute()
        grid = self.engine.grid_ids()
        return grid


game = FireClock((1920, 1080), (160, 90))
game.run()
