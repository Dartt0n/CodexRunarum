import numpy as np

from codexrunarum.core import elements
from codexrunarum.core.engine import Engine
from codexrunarum.examples.base import DemoBase


class StoneFall(DemoBase):
    def engine_init(self):
        self.engine = Engine(self.grid_rows, self.grid_cols)

        for _ in range(int(self.grid_rows * self.grid_cols * 0.01)):
            r = np.random.randint(self.grid_rows)
            c = np.random.randint(self.grid_cols)
            temperature = np.random.random() * 5  # Temperature from 0 to 1
            direction = np.random.rand(2) * np.random.randint(
                10, self.grid_cols
            )  # Random 2D direction vector
            self.engine.spawn_element_at(r, c, elements.Fire(temperature, direction))

        for _ in range(int(self.grid_rows * self.grid_cols * 0.01)):
            r = np.random.randint(self.grid_rows)
            c = np.random.randint(self.grid_cols)
            volume = np.random.randint(1, 6)  # Volume from 1 to 5
            direction = np.random.randint(
                -1, 2, 2
            )  # Random direction unit vector in Moore neighborhood
            momentum = np.random.randint(1, 16)  # Momentum from 1 to 15
            self.engine.spawn_element_at(
                r, c, elements.Water(volume, direction, momentum)
            )

        for _ in range(int(self.grid_rows * self.grid_cols * 0.03)):
            r = np.random.randint(self.grid_rows)
            c = np.random.randint(self.grid_cols)
            hardness = np.random.randint(1, 51)  # Hardness from 1 to 50
            self.engine.spawn_element_at(r, c, elements.Stone(hardness))

        for _ in range(int(self.grid_rows * self.grid_cols * 0.01)):
            r = np.random.randint(self.grid_rows)
            c = np.random.randint(self.grid_cols)
            health = np.random.randint(1, 4)  # Health from 1 to 3
            direction = np.random.randint(
                -1, 2, 2
            )  # Random direction unit vector in Moore neighborhood
            self.engine.spawn_element_at(r, c, elements.Tree(health, direction, None))

        self.engine_calls = 0

    def engine_call(self):
        if self.engine_calls % 50 == 0:
            self.engine_init()
        self.engine_calls += 1

        for _ in range(int(self.grid_rows * self.grid_cols * 0.03)):
            r = np.random.randint(self.grid_rows)
            c = np.random.randint(self.grid_cols)
            hardness = np.random.randint(1, 51)  # Hardness from 1 to 50
            self.engine.spawn_element_at(r, c, elements.Stone(hardness))

        self.engine.evolute()
        grid = self.engine.grid_ids()
        return grid


game = StoneFall((800, 600), (800 // 16, 600 // 16))
game.run()
