import numpy as np


class BaseElement:
    energy: float
    velocity: np.ndarray[np.float32]

    def __init__(self, energy: float, velocity: np.ndarray[np.float32]):
        self.energy = energy
        self.velocity = velocity
