import streamlit as st
import numpy as np
from src.models import Drone, PID
from src.utils.plot import plot_simulation_data
from src.env import (
    TIME_STEP,
    TOTAL_SIM_TIME,
    DESIRED_POSITION,
    DRONE_MASS,
    INITIAL_POSITION,
    KP,
    KI,
    KD,
)


def run_simulation(kp, ki, kd):
    """Runs the drone simulation with the given PID constants."""
    time_points = np.arange(0, TOTAL_SIM_TIME, TIME_STEP)

    initial_pos = np.array(INITIAL_POSITION)
    desired_pos = np.array(DESIRED_POSITION)

    if initial_pos.shape != desired_pos.shape:
        raise ValueError("Initial and desired positions must have the same shape.")

    drone = Drone(mass=DRONE_MASS, initial_position=initial_pos)

    num_dimensions = len(initial_pos)
    pid_controllers = [
        PID(Kp=kp, Ki=ki, Kd=kd, desired_position=desired_pos[i])
        for i in range(num_dimensions)
    ]

    drone_path = []
    forces = []
    p_components = []
    i_components = []
    d_components = []

    # Run simulation
    for _ in time_points:
        force_vector = np.zeros(num_dimensions)
        p_vec, i_vec, d_vec = (
            np.zeros(num_dimensions),
            np.zeros(num_dimensions),
            np.zeros(num_dimensions),
        )

        for i in range(num_dimensions):
            force_vector[i] = pid_controllers[i].compute_force(
                drone.position[i], TIME_STEP
            )
            p_vec[i] = pid_controllers[i].pid_P
            i_vec[i] = pid_controllers[i].pid_I
            d_vec[i] = pid_controllers[i].pid_D

        drone.apply_force(force_vector, TIME_STEP)

        drone_path.append(drone.position.copy())
        forces.append(force_vector)
        p_components.append(p_vec)
        i_components.append(i_vec)
        d_components.append(d_vec)

    fig = plot_simulation_data(
        time_points,
        drone_path,
        forces,
        p_components,
        i_components,
        d_components,
        desired_pos,
    )
    return fig


# Setup streamlit app
st.set_page_config(layout="wide")
st.title("Drone PID Controller Simulation")
st.write(
    "Use the sliders in the sidebar to tune the PID controller's gains (Kp, Ki, Kd) "
    "and observe the effect on the drone's stability in real-time."
)

# PID constants
st.sidebar.header("PID Constants")
kp = st.sidebar.slider("Kp (Proportional Gain)", 0.0, 2.0, KP, 0.05)
ki = st.sidebar.slider("Ki (Integral Gain)", 0.0, 1.0, KI, 0.01)
kd = st.sidebar.slider("Kd (Derivative Gain)", 0.0, 2.0, KD, 0.05)

# Run simulation and display the plot
simulation_fig = run_simulation(kp, ki, kd)
st.pyplot(simulation_fig)
