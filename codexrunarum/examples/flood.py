import time

import numpy as np
import pygame

from codexrunarum.core import elements
from codexrunarum.core.engine import Engine


class PygameClass:
    def __init__(self, screen_size, grid_size):
        pygame.init()
        self.grid_rows, self.grid_cols = grid_size
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()

        self.colors = {
            0: (0, 0, 0),
            elements.Fire.id: (255, 0, 0),
            elements.Stone.id: (128, 128, 128),
            elements.Tree.id: (0, 255, 0),
            elements.Water.id: (0, 0, 255),
        }
        self.cell_size = screen_size[0] // grid_size[0], screen_size[1] // grid_size[1]
        self.engine_init()

    def draw_grid(self, grid):
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                pygame.draw.rect(
                    self.screen,
                    self.colors[grid[i, j]],
                    (
                        i * self.cell_size[0],
                        j * self.cell_size[1],
                        self.cell_size[0],
                        self.cell_size[1],
                    ),
                )

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.fill((0, 0, 0))

            grid = self.engine_call()
            self.draw_grid(grid)

            pygame.display.flip()
            self.clock.tick(60)

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

        self.engine.evolute()
        grid = self.engine.grid_ids()
        return grid


game = PygameClass((800, 600), (800 // 16, 600 // 16))
game.run()
