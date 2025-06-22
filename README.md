<p align="center">
  <img src="https://github.com/user-attachments/assets/b60290c2-2efd-4693-82c9-de2b34a36c50" />
</p>

# Drone PID Simulator

A simulator to visualize the movement of a drone controlled by PID controllers. Users can tune the controller gains and drone properties in real-time and observe the impact on its flight path and stability.

## How it Works
The simulation calculates the necessary forces to guide a drone from a starting point to a desired position. For each dimension (X, Y, Z), a separate PID controller computes a force based on the drone's current position and velocity. These forces are then applied to the drone model, and the simulation iteratively updates its position over time.

To make things interesting, an external force can also be applied. We can then see how the drone and it's PID controllers behave.

The dashboard is built with [Streamlit](https://streamlit.io/) and the plots are generated using [Matplotlib](https://matplotlib.org/).

## Features

- **Interactive PID Tuning:** Adjust Proportional (Kp), Integral (Ki), and Derivative (Kd) gains using sliders.
- **Real-time Visualization:** Instantly see how changes to the PID gains or drone mass affect the drone's behavior.
- **3D Drone Path:** View the drone's trajectory from its start to its target position in a 3D plot.
- **Detailed 2D Plots:** Analyze the drone's position and the PID force components over time for each dimension.
- **Configurable Simulation:** Easily change default parameters like initial/desired positions, simulation time, and external forces directly in the source code.

## Getting Started

Dependencies are managed with Pipenv. Therefore cloning and downloading the packages will get your environment sorted.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/michaelgreen-0/drone-pid-simulation.git
    cd drone-simulation
    ```

2.  **Install the packages and start pipenv shell:**
    ```bash
    pipenv install
    pipenv shell
    ```

3. **Update environment variables**: Update your desired default values in the src/env.py file.

Launch the Streamlit application by running:
```bash
streamlit run dashboard.py
```
Your web browser should open with the dashboard automatically.

## Environment Variables

Analysis is given for any number of dimensions. 2D, 3D, 4D ... etc. The lowest level is 2 dimensions.

Flight paths are given for all dimensions in 3D space. However, from 4D onrwards, we only plot the first 3 dimensions.

This is based on what you feed into the src/env.py file.

## License

This project is licensed under the MIT License - see the LICENSE file for details
