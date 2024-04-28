import os
import time

import numpy as np

from .core.elements import Fire, Stone
from .core.engine import Engine

stone_tube = np.array(
    [
        [Stone(500), Stone(500), Stone(500), Stone(500), None, None],
        [Stone(500), None, None, Stone(500), None, None],
        [None, None, None, None, None, None],
        [Stone(500), None, None, Stone(500), None, None],
        [Stone(500), Stone(500), Stone(500), Stone(500), None, None],
    ]
)

if __name__ == "__main__":
    engine = Engine(15, 45)

    start_time = time.time()
    iters = 0

    engine.spawn_pattern(5, 0, stone_tube)
    while True:
        engine.spawn_element_at(7, 0, Fire(1.0, np.array((0.0, 100.0))))
        engine.spawn_element_at(7, 44, Fire(1.0, np.array((0.0, -100.0))))
        os.system("clear")
        engine.print_state(
            {Fire.id: "red", Stone.id: "white"},
            spacing="",
        )
        engine.evolute()

        time.sleep(1 / 15)

        iters += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            ips = iters / elapsed_time
            print("fps =", ips)
