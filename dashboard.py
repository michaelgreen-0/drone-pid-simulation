import streamlit as st
import numpy as np
from src.models import Drone, PID
from src.utils.plot import plot_simulation_data
from src.env import (
    TIME_STEP,
    TOTAL_SIM_TIME,
    DESIRED_Y_POSITION,
    DRONE_MASS,
    INITIAL_POSITION,
    KP,
    KI,
    KD,
)


def run_simulation(kp, ki, kd):
    """Runs the drone simulation with the given PID constants."""
    time_points = np.arange(0, TOTAL_SIM_TIME, TIME_STEP)

    drone = Drone(mass=DRONE_MASS, initial_position=INITIAL_POSITION)
    pid_y = PID(Kp=kp, Ki=ki, Kd=kd, desired_position=DESIRED_Y_POSITION)

    drone_path_y = []
    forces_y = []
    p_components = []
    i_components = []
    d_components = []

    # Run simulation
    for _ in time_points:
        force_y = pid_y.compute_force(drone.position, TIME_STEP)
        drone.apply_force(force_y, TIME_STEP)

        drone_path_y.append(drone.position)
        forces_y.append(force_y)
        p_components.append(pid_y.pid_P)
        i_components.append(pid_y.pid_I)
        d_components.append(pid_y.pid_D)

    fig = plot_simulation_data(
        time_points,
        drone_path_y,
        forces_y,
        p_components,
        i_components,
        d_components,
        DESIRED_Y_POSITION,
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
