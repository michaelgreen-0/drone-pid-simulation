import matplotlib.pyplot as plt
import numpy as np


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
