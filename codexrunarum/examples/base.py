import random
from abc import ABC, abstractmethod
from itertools import cycle

import numpy as np
import pygame

from codexrunarum.core import elements


def rgb(r, g, b):
    return (r, g, b)


class DemoBase(ABC):
    def __init__(
        self, screen_size: tuple[int, int], grid_size: tuple[int, int], fps: int = 30
    ):
        pygame.init()
        self.grid_cols, self.grid_rows = grid_size
        self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.cell_size = screen_size[0] // grid_size[0], screen_size[1] // grid_size[1]
        self.engine_init()

        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def get_color(self, id):
        COLOR_MAP = {
            0: [(0, 0, 0)],
            elements.Fire.id: [
                rgb(255, 0, 0),
                rgb(255, 46, 0),
                rgb(255, 67, 0),
                rgb(255, 83, 0),
                rgb(255, 97, 0),
                rgb(255, 110, 0),
                rgb(255, 122, 0),
                rgb(255, 133, 0),
                rgb(255, 143, 0),
                rgb(255, 153, 0),
            ],
            elements.Stone.id: [
                rgb(209, 202, 202),
                rgb(201, 190, 191),
                rgb(194, 178, 181),
                rgb(186, 166, 172),
                rgb(177, 154, 164),
                rgb(167, 143, 156),
                rgb(157, 132, 150),
                rgb(146, 122, 144),
                rgb(135, 111, 138),
                rgb(122, 102, 133),
            ],
            elements.Tree.id: [
                rgb(76, 148, 0),
                rgb(84, 159, 1),
                rgb(92, 171, 1),
                rgb(101, 183, 2),
                rgb(110, 194, 2),
                rgb(119, 206, 2),
                rgb(128, 218, 2),
                rgb(138, 230, 2),
                rgb(147, 243, 1),
                rgb(157, 255, 0),
            ],
            elements.Water.id: [
                rgb(65, 42, 206),
                rgb(62, 46, 209),
                rgb(58, 49, 212),
                rgb(54, 52, 215),
                rgb(50, 55, 217),
                rgb(45, 58, 220),
                rgb(39, 61, 223),
                rgb(32, 64, 226),
                rgb(23, 67, 228),
                rgb(8, 70, 231),
            ],
        }

        return random.choice(COLOR_MAP[id])

    def draw_grid(self, grid):
        for row in range(grid.shape[1]):
            for col in range(grid.shape[0]):
                pygame.draw.rect(
                    self.screen,
                    self.get_color(grid[col, row]),
                    (
                        row * self.cell_size[1],
                        col * self.cell_size[0],
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

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.quit()
                    return

            self.screen.fill((0, 0, 0))

            grid = self.engine_call()
            self.draw_grid(grid)

            pygame.display.flip()
            self.clock.tick(self.fps)

    @abstractmethod
    def engine_init(): ...

    @abstractmethod
    def engine_call(): ...
