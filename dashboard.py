import streamlit as st
import os
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
    EXTERNAL_FORCE_VECTOR,  # New: Import external force
)


def run_simulation(kp, ki, kd):
    """Runs the drone simulation with the given PID constants."""
    time_points = np.arange(0, TOTAL_SIM_TIME, TIME_STEP)

    initial_pos = np.array(INITIAL_POSITION)
    desired_pos = np.array(DESIRED_POSITION)
    external_force = np.array(EXTERNAL_FORCE_VECTOR)

    # Validate inputs
    if initial_pos.shape != desired_pos.shape:
        raise ValueError("Initial and desired positions must have the same shape.")
    if external_force.shape != initial_pos.shape:
        raise ValueError("External force vector must match simulation dimensions.")

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
        pid_force_vector = np.zeros(num_dimensions)
        p_vec, i_vec, d_vec = (
            np.zeros(num_dimensions),
            np.zeros(num_dimensions),
            np.zeros(num_dimensions),
        )

        for i in range(num_dimensions):
            pid_force_vector[i] = pid_controllers[i].compute_force(
                drone.position[i], TIME_STEP
            )
            p_vec[i] = pid_controllers[i].pid_P
            i_vec[i] = pid_controllers[i].pid_I
            d_vec[i] = pid_controllers[i].pid_D

        total_force_vector = pid_force_vector + external_force
        drone.apply_force(total_force_vector, TIME_STEP)

        drone_path.append(drone.position.copy())
        forces.append(total_force_vector)
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


st.set_page_config(layout="wide")
st.title("Drone PID Controller Simulation")
st.write(
    "Use the sliders in the sidebar to tune the PID controller's gains (Kp, Ki, Kd) "
    "and observe the effect on the drone's stability and path."
)

# PID constants
st.sidebar.header("PID Constants")
kp = st.sidebar.slider("Kp (Proportional)", 0.0, KP * 2, KP, 0.05)
ki = st.sidebar.slider("Ki (Integral)", 0.0, KI * 2, KI, 0.01)
kd = st.sidebar.slider("Kd (Derivative)", 0.0, KD * 2, KD, 0.05)

col1, col2 = st.columns(2)

with col1:
    st.header("Time Series Data")
    simulation_fig = run_simulation(kp, ki, kd)
    st.pyplot(simulation_fig)

with col2:
    st.header("Drone Path (2D/3D)")
    path_image_filename = "drone_path.png"
    if os.path.exists(path_image_filename):
        st.image(path_image_filename)
    else:
        st.info("Path plot is available for 2D and 3D simulations.")
