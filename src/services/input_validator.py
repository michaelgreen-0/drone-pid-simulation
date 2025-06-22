import numpy as np
from ..logger import Logger


class Validator:
    def __init__(
        self,
        kp: float,
        ki: float,
        kd: float,
        time_step: float,
        total_sim_time: float,
        drone_mass: float,
        desired_position: list,
        initial_position: list,
        external_force_vector: list,
        logger: Logger,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.time_step = time_step
        self.total_sim_time = total_sim_time
        self.drone_mass = drone_mass
        self.desired_position = desired_position
        self.initial_position = initial_position
        self.external_force_vector = external_force_vector
        self.logger = logger

    def validate_all(self):
        self.logger.info("Running input validation...")
        self.__validate_pid_gains()
        self.__validate_time()
        self.__validate_array_lengths()
        self.__validate_drone_mass()
        self.logger.info("Input validation successful.")

    def __validate_pid_gains(self):
        if not all(gain >= 0 for gain in [self.kp, self.ki, self.kd]):
            raise ValueError("PID gains (Kp, Ki, Kd) must be non-negative.")

    def __validate_time(self):
        if self.time_step <= 0 or self.total_sim_time <= 0:
            raise ValueError("Time step and total simulation time must be positive.")

    def __validate_array_lengths(self):
        len_initial_position = len(self.initial_position)
        len_desired_position = len(self.desired_position)
        len_external_force = len(self.external_force_vector)

        if not (len_initial_position == len_desired_position == len_external_force):
            raise ValueError(
                "Shape mismatch: Initial position, desired position, and external force vector must all have the same dimensions."
            )

    def __validate_drone_mass(self):
        if self.drone_mass <= 0:
            raise ValueError("Drone mass must be a positive value.")
