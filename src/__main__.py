import numpy as np
from .models import Drone, PID
from .utils.plot import plot_simulation_data
from .env import (
    TIME_STEP,
    TOTAL_SIM_TIME,
    DESIRED_Y_POSITION,
    DRONE_MASS,
    INITIAL_POSITION,
    KP,
    KI,
    KD,
)


if __name__ == "__main__":
    time_points = np.arange(0, TOTAL_SIM_TIME, TIME_STEP)

    drone = Drone(mass=DRONE_MASS, initial_position=INITIAL_POSITION)
    pid_y = PID(Kp=KP, Ki=KI, Kd=KD, desired_position=DESIRED_Y_POSITION)

    drone_path_y = []
    forces_y = []
    p_components = []
    i_components = []
    d_components = []

    for t in time_points:
        force_y = pid_y.compute_force(drone.position, TIME_STEP)
        drone.apply_force(force_y, TIME_STEP)

        drone_path_y.append(drone.position)
        forces_y.append(force_y)
        p_components.append(pid_y.pid_P)
        i_components.append(pid_y.pid_I)
        d_components.append(pid_y.pid_D)

    plot_simulation_data(
        time_points,
        drone_path_y,
        forces_y,
        p_components,
        i_components,
        d_components,
        DESIRED_Y_POSITION,
    )
