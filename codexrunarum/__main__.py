import os
import time

import numpy as np

from codexrunarum.core.elements import Fire, Stone, Water
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
    engine = Engine(15, 45)

    start_time = time.time()
    iters = 0

    # engine.spawn_pattern(1, 2, stone_tube)
    engine.spawn_element_at(7, 0, Water(10, np.array((0, 1)), 10))
    engine.spawn_element_at(7, 35, Fire(1.0, np.array((0.0, -100.0))))
    while True:
        os.system("clear")
        engine.print_state(
            {Fire.id: "red", Stone.id: "white", Water.id: "blue"},
            spacing="",
        )
        engine.evolute()

        iters += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            ips = iters / elapsed_time
            print("fps =", ips)

        # time.sleep(1 / 15)
        input()
