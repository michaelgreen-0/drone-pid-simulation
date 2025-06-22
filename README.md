<p align="center">
  <img src="https://github.com/user-attachments/assets/bf0757d4-8981-447b-82ca-775d5a28f6a5" />
</p>

# Drone PID Simulator

A simulator to visualize the force-based movement of a drone controlled by PID controllers. Users can tune the controller gains and drone properties in real-time and observe the impact on its flight path and stability.

## How it Works
The simulation calculates the necessary forces to guide a drone from a starting point to a desired position. For each dimension, a separate PID controller computes a force based on the drone's current position and velocity. These forces are then applied to the drone model, and the simulation iteratively updates its position over time.

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
    cd drone-pid-simulation
    ```

2.  **Install the packages and start pipenv shell:**
    ```bash
    pipenv install
    pipenv shell
    ```

3. **Update environment variables**: Update your desired variables in the src/env.py file. This covers properties relating to the drone, PID controllers, initial and desired positions, external forces, and the simulation itself.

The below example variables are for a 3D simulation. But this can be any number of dimensions starting from 2D.


| Environment Variable                | Example | Description                                                                                             |
| :---------------------- | :---------------- | :------------------------------------------------------------------------------------------------------ |
| `TIME_STEP`             | `0.01`            | The time increment for each step of the simulation (in seconds).                                        |
| `TOTAL_SIM_TIME`        | `10`            | The total duration of the simulation (in seconds).                                                      |
| `DRONE_MASS`            | `1.0`             | The mass of the drone (in kilograms). Affects how forces translate to acceleration.                     |
| `DESIRED_POSITION`      | `[0.0, 0.0, 0.0]` | The target position the drone aims to reach.                  |
| `INITIAL_POSITION`      | `[10.0, 10.0, 10.0]` | The starting position of the drone.                           |
| `EXTERNAL_FORCE_VECTOR` | `[0.0, 0.0, 0.0]` | A constant external force applied to the drone throughout the simulation.          |
| `KP`                    | `1.0`             | Proportional gain for the PID controller. Controls response to current error.                           |
| `KI`                    | `0.1`             | Integral gain for the PID controller. Addresses accumulated error over time.                            |
| `KD`                    | `0.5`             | Derivative gain for the PID controller. Dampens oscillations based on rate of error change.             |


Launch the Streamlit application by running:
```bash
streamlit run src/dashboard.py
```
Your web browser should open with the dashboard automatically.

## Environment Variables

Analysis is given for any number of dimensions. 2D, 3D, 4D ... etc. The lowest level is 2 dimensions.

Flight paths are given for all dimensions in 3D space. However, from 4D onwards, we only plot the first 3 dimensions.

This is based on what you feed into the src/env.py file.

## License

This project is licensed under the MIT License - see the LICENSE file for details
