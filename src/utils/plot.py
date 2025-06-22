import matplotlib

matplotlib.use("Agg")  # Use a non-interactive backend suitable for scripts
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # For 3D plots


def plot_drone_path(positions, desired_pos, output_filename="drone_path.png"):
    """
    Plots the drone's path in a 3D space.
    For 2D simulations, the path is plotted on the z=0 plane.
    """
    num_dimensions = positions.shape[1]

    # Don't plot for 1D simulations
    if num_dimensions == 1:
        return

    # Prepare data for 3D plotting
    if num_dimensions == 2:
        # Add a Z-axis of zeros to the 2D data
        z_zeros = np.zeros((positions.shape[0], 1))
        positions_3d = np.hstack((positions, z_zeros))
        desired_pos_3d = np.append(desired_pos, 0)
    else:
        # Use the first 3 dimensions for plotting if more are available
        positions_3d = positions[:, :3]
        desired_pos_3d = desired_pos[:3]

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Plot path
    ax.plot(
        positions_3d[:, 0],
        positions_3d[:, 1],
        positions_3d[:, 2],
        label="Drone Path",
        color="blue",
        linewidth=2,
    )

    # Point - Desired position (red)
    ax.scatter(
        desired_pos_3d[0],
        desired_pos_3d[1],
        desired_pos_3d[2],
        c="red",
        marker="x",
        s=100,
        label="Desired",
    )

    # Point - Start position (green)
    ax.scatter(
        positions_3d[0, 0],
        positions_3d[0, 1],
        positions_3d[0, 2],
        c="green",
        marker="o",
        s=100,
        label="Start",
    )

    ax.set_xlabel("X Position (m)")
    ax.set_ylabel("Y Position (m)")
    ax.set_zlabel("Z Position (m)")
    ax.set_title("Drone Path"), ax.legend()

    # Save plot as png
    plt.savefig(output_filename)
    plt.close(fig)


def plot_simulation_data(
    time_points, positions, forces, p_comps, i_comps, d_comps, desired_pos
):
    positions = np.array(positions)
    forces = np.array(forces)
    p_comps = np.array(p_comps)
    i_comps = np.array(i_comps)
    d_comps = np.array(d_comps)
    desired_pos = np.array(desired_pos)

    num_dimensions = positions.shape[1] if positions.ndim > 1 else 1

    # Generate and save the drone path animation to a file
    plot_drone_path(positions, desired_pos)

    # Plot setup
    # Create a plot for each dimension
    fig, axes = plt.subplots(
        num_dimensions, 2, figsize=(12, 4 * num_dimensions), sharex=True, squeeze=False
    )
    plt.style.use("seaborn-v0_8-whitegrid")
    dim_labels = ["X", "Y", "Z"]

    for i in range(num_dimensions):
        ax1 = axes[i, 0]
        ax2 = axes[i, 1]
        dim_label = dim_labels[i] if i < len(dim_labels) else f"Dim {i+1}"

        # Position vs time
        pos_data = positions[:, i] if num_dimensions > 1 else positions
        ax1.plot(
            time_points, pos_data, label="Drone Position", color="blue", linewidth=2
        )
        ax1.axhline(
            y=desired_pos[i], color="red", linestyle="--", label="Desired Position"
        )
        ax1.set_ylabel(f"{dim_label}-Position (m)")
        ax1.set_title(f"Drone Position ({dim_label})")
        ax1.legend()

        # Force vs time
        ax2.plot(
            time_points,
            forces[:, i] if num_dimensions > 1 else forces,
            label="Total Force (P+I+D)",
            color="black",
            linewidth=2.5,
        )
        ax2.plot(
            time_points,
            p_comps[:, i] if num_dimensions > 1 else p_comps,
            label="Proportional (P)",
            linestyle=":",
        )
        ax2.plot(
            time_points,
            i_comps[:, i] if num_dimensions > 1 else i_comps,
            label="Integral (I)",
            linestyle=":",
        )
        ax2.plot(
            time_points,
            d_comps[:, i] if num_dimensions > 1 else d_comps,
            label="Derivative (D)",
            linestyle=":",
        )
        ax2.set_ylabel("Force (N)")
        ax2.set_title(f"PID Force Components ({dim_label})")
        ax2.legend()

    axes[-1, 0].set_xlabel("Time (s)")
    axes[-1, 1].set_xlabel("Time (s)")

    plt.tight_layout()
    return fig
