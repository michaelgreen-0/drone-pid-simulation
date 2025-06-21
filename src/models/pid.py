import numpy as np


class PID:
    def __init__(self, Kp: float, Ki: float, Kd: float, desired_position: float):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.desired_position = desired_position
        self.pid_P = 0
        self.pid_I = 0
        self.pid_D = 0

        self.__integral = 0
        self.__previous_error = 0

    def compute_force(self, current_position: float, dt: float):
        error = self.desired_position - current_position

        self.pid_P = self.Kp * error

        self.__integral += error * dt  # Small dt means approximate integral as square
        self.pid_I = self.Ki * self.__integral

        derivative = (error - self.__previous_error) / dt  # de/dt
        self.pid_D = self.Kd * derivative

        self.__previous_error = error

        return self.pid_P + self.pid_I + self.pid_D
