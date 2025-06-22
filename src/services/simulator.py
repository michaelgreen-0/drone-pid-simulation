import numpy as np
from models import Drone, PID
from logger import Logger


class Simulator:
    def __init__(
        self,
        kp: float,
        ki: float,
        kd: float,
        time_points: np.ndarray,
        drone_mass: float,
        desired_position: np.ndarray,
        initial_position: np.ndarray,
        external_force_vector: np.ndarray,
        logger: Logger,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.time_points = time_points
        self.time_step = time_points[1] - time_points[0]
        self.drone_mass = drone_mass
        self.desired_position = desired_position
        self.initial_position = initial_position
        self.external_force_vector = external_force_vector
        self.logger = logger

    def run_simulation(self):
        initial_pos = np.array(self.initial_position)
        desired_pos = np.array(self.desired_position)
        external_force = np.array(self.external_force_vector)

        # Validate inputs
        if initial_pos.shape != desired_pos.shape:
            raise ValueError("Initial and desired positions must have the same shape.")
        if external_force.shape != initial_pos.shape:
            raise ValueError("External force vector must match simulation dimensions.")

        # Setup drone and PID controller objects. There is 1 PID controller for each dimension.
        drone = Drone(mass=self.drone_mass, initial_position=initial_pos)
        num_dimensions = len(initial_pos)
        pid_controllers = [
            PID(Kp=self.kp, Ki=self.ki, Kd=self.kd, desired_position=desired_pos[i])
            for i in range(num_dimensions)
        ]

        # Lists for storing history of drone movement
        num_steps = len(self.time_points)
        drone_path = np.zeros((num_steps, num_dimensions))
        drone_forces = np.zeros((num_steps, num_dimensions))
        p_components = np.zeros((num_steps, num_dimensions))
        i_components = np.zeros((num_steps, num_dimensions))
        d_components = np.zeros((num_steps, num_dimensions))

        # Run simulation
        self.logger.info("Running simulation...")
        for t, _ in enumerate(self.time_points):
            # Reset force and PID component vectors on each iteration
            pid_force_vector = np.zeros(num_dimensions)
            p_vec, i_vec, d_vec = (
                np.zeros(num_dimensions),
                np.zeros(num_dimensions),
                np.zeros(num_dimensions),
            )

            # Calculate force for each PID component in each dimension
            for d in range(num_dimensions):
                pid_force_vector[d] = pid_controllers[d].compute_force(
                    drone.position[d], self.time_step
                )
                p_vec[d] = pid_controllers[d].pid_P
                i_vec[d] = pid_controllers[d].pid_I
                d_vec[d] = pid_controllers[d].pid_D

            # Calculate total force with external force also applied
            total_force_vector = pid_force_vector + external_force
            drone.apply_force(total_force_vector, self.time_step)

            # Update history lists
            drone_path[t] = drone.position.copy()
            drone_forces[t] = total_force_vector
            p_components[t] = p_vec
            i_components[t] = i_vec
            d_components[t] = d_vec

        self.logger.info("Simulation completed.")

        return (
            drone_path,
            drone_forces,
            p_components,
            i_components,
            d_components,
        )
