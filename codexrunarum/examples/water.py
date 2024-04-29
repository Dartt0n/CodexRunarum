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
            self.clock.tick(1)

    def engine_init(self):
        self.engine = Engine(self.grid_rows, self.grid_cols)

        self.engine.spawn_element_at(
            self.grid_rows // 2, 0, elements.Water(4, np.array((0, 1)), 10.0)
        )

        self.engine_calls = 0

    def engine_call(self):
        if self.engine_calls % 200 == 0:
            self.engine_init()
        self.engine_calls += 1

        self.engine.evolute()
        grid = self.engine.grid_ids()
        return grid


game = PygameClass((800, 600), (800 // 16, 600 // 16))
game.run()
