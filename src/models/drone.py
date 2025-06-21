class Drone:
    def __init__(self, mass: float, initial_position: float):
        self.mass = mass
        self.position = initial_position
        self.velocity = 0.0

    def apply_force(self, force: float, dt: float):
        acceleration = force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
