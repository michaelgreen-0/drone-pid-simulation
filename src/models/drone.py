import numpy as np


class Drone:
    def __init__(self, mass: float, initial_position: np.ndarray):
        self.mass = mass
        self.position = np.array(initial_position, dtype=float)
        self.velocity = np.zeros_like(self.position)

    def apply_force(self, force: np.ndarray, dt: float):
        acceleration = force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
