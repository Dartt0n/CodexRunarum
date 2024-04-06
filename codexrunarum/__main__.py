import os
import time

import numpy as np

from codexrunarum.core.elements import Fire, Rock, Void, Water
from codexrunarum.core.engine import Engine

if __name__ == "__main__":
    engine = Engine(15, 25)

    while True:
        engine.spawn_element_at(7, 0, Fire(np.array((0.0, 15.0))))
        os.system("clear")
        engine.print_state(
            {Fire.id: "red", Void.id: "black", Water.id: "blue", Rock.id: "white"},
            spacing="",
        )
        time.sleep(0.2)
        engine.evolute()
