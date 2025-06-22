import streamlit as st
import numpy as np
from logger import Logger
from services import Simulator, Plotter, Validator
from env import (
    TIME_STEP,
    TOTAL_SIM_TIME,
    DESIRED_POSITION,
    DRONE_MASS,
    INITIAL_POSITION,
    KP,
    KI,
    KD,
    EXTERNAL_FORCE_VECTOR,
)

logger = Logger()

Validator(
    kp=KP,
    ki=KI,
    kd=KD,
    time_step=TIME_STEP,
    total_sim_time=TOTAL_SIM_TIME,
    drone_mass=DRONE_MASS,
    desired_position=DESIRED_POSITION,
    initial_position=INITIAL_POSITION,
    external_force_vector=EXTERNAL_FORCE_VECTOR,
    logger=Logger(),
).validate_all()

st.set_page_config(layout="wide")
st.title("Drone PID Controller Simulation")
st.write(
    """
    Use the sliders in the sidebar to tune the PID controller's gains (Kp, Ki, Kd)
    and observe the effect on the drone's stability and path.
    """
)

# PID constants (Slider min and max are 0 and 2*constant)
st.sidebar.header("PID Constants")
kp = st.sidebar.slider("Kp (Proportional)", 0.0, KP * 2, KP, 0.05)
ki = st.sidebar.slider("Ki (Integral)", 0.0, KI * 2, KI, 0.01)
kd = st.sidebar.slider("Kd (Derivative)", 0.0, KD * 2, KD, 0.05)

st.sidebar.header("Drone Properties")
drone_mass = st.sidebar.slider(
    "Drone Mass (kg)", 0.1, float(DRONE_MASS * 2), float(DRONE_MASS), 0.1
)

logger.info("Setting up simulator...")
time_points = np.arange(0, TOTAL_SIM_TIME, TIME_STEP)
simulator = Simulator(
    kp=kp,
    ki=ki,
    kd=kd,
    time_points=time_points,
    drone_mass=drone_mass,
    desired_position=DESIRED_POSITION,
    initial_position=INITIAL_POSITION,
    external_force_vector=EXTERNAL_FORCE_VECTOR,
    logger=logger,
)
drone_path, drone_forces, p_components, i_components, d_components = (
    simulator.run_simulation()
)

# Plot results of simulation
plotter = Plotter(
    time_points,
    drone_path,
    drone_forces,
    p_components,
    i_components,
    d_components,
    DESIRED_POSITION,
)
fig_movement_charts = plotter.plot_charts()
fig_drone_path = plotter.plot_drone_path()

col1, col2 = st.columns(2)
with col1:
    st.header("Drone Position and Forces")
    st.pyplot(fig_movement_charts)

with col2:
    st.header("Drone Path")
    st.pyplot(fig_drone_path)
