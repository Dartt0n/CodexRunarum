import os
import time

import numpy as np

from codexrunarum.core.elements import Fire, Stone, Tree, Water
from codexrunarum.core.engine import Engine

stone_tube = np.array(
    [
        [Stone(5), Stone(5), Stone(5), Stone(5)],
        [Stone(5), None, None, None],
        [Stone(5), None, Stone(5), Stone(5)],
        [Stone(5), None, Stone(5), None],
        [Stone(5), None, Stone(5), None],
        [Stone(5), None, Stone(5), None],
        [Stone(5), None, Stone(5), None],
        [None, None, Stone(5), None],
        [Stone(5), Stone(5), Stone(5), None],
    ]
)

if __name__ == "__main__":
    GRID_ROWS = 90
    GIRD_COLS = 160

    engine = Engine(GRID_ROWS, GIRD_COLS)

    start_time = time.time()
    iters = 0

    # engine.spawn_pattern(1, 2, stone_tube)

    while True:
        for _ in range(30):
            r = np.random.randint(GRID_ROWS)
            c = np.random.randint(GIRD_COLS)
            engine.spawn_element_at(r, c, Water(0.1, np.array((0, 0)), 0.0))

        engine.spawn_element_at(
            GRID_ROWS // 2 + 1, 0, Water(0.1, np.array((0, 0)), 0.0)
        )
        engine.spawn_element_at(GRID_ROWS // 2, 0, Tree(1, np.array((0, 1), None)))

        for i in range(200):
            engine.spawn_element_at(
                GRID_ROWS // 2, GIRD_COLS - 1, Fire(1, np.array((0, -GIRD_COLS // 2)))
            )
            # os.system("clear")
            # engine.print_state(
            #     {Fire.id: "red", Stone.id: "white", Water.id: "blue", Tree.id: "green"},
            #     spacing="",
            # )
            engine.evolute()

            iters += 1
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                ips = iters / elapsed_time
                print("fps =", ips)
