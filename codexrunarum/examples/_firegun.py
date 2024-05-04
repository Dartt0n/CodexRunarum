import numpy as np

from codexrunarum.core import elements
from codexrunarum.core.engine import Engine
from codexrunarum.examples.base import DemoBase


class FireGun(DemoBase):
    def engine_init(self):
        self.engine = Engine(self.grid_rows, self.grid_cols)

        for i in range(20):
            self.engine.spawn_element_at(
                self.grid_rows // 2 - 8,
                i + 4,
                elements.Stone(100.0),
            )
            self.engine.spawn_element_at(
                self.grid_rows // 2 - 6,
                i + 4,
                elements.Water(1, np.array((0, 0)), 1.0),
            )
            self.engine.spawn_element_at(
                self.grid_rows // 2 - 4,
                i + 4,
                elements.Tree(1, np.array((1, 0))),
            )

            if i % 3 != 0:
                self.engine.spawn_element_at(
                    self.grid_rows // 2 - 3,
                    i + 4,
                    elements.Stone(50.0),
                )

            if i % 3 != 0:
                self.engine.spawn_element_at(
                    self.grid_rows // 2 + 3,
                    i + 4,
                    elements.Stone(100.0),
                )

            self.engine.spawn_element_at(
                self.grid_rows // 2 + 4,
                i + 4,
                elements.Tree(1, np.array((-1, 0))),
            )
            self.engine.spawn_element_at(
                self.grid_rows // 2 + 6,
                i + 4,
                elements.Water(1, np.array((0, 0)), 1.0),
            )
            self.engine.spawn_element_at(
                self.grid_rows // 2 + 8,
                i + 4,
                elements.Stone(100.0),
            )

        for i in range(16):
            offset = self.grid_rows // 2 - 8 + i
            if offset <= self.grid_rows // 2 - 3 or offset >= self.grid_rows // 2 + 3:
                self.engine.spawn_element_at(offset, 4, elements.Stone(50.0))

    def engine_call(self):
        self.engine.evolute()
        grid = self.engine.grid_ids()

        self.engine.spawn_element_at(
            self.grid_rows // 2, 0, elements.Fire(2, np.array((0, 20)))
        )

        return grid


game = FireGun((1920, 1080), (80, 45))
game.run()
