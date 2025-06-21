import matplotlib.pyplot as plt


def plot_simulation_data(
    time_points, positions, forces, p_comps, i_comps, d_comps, desired_pos
):
    # Plot setup
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 4), sharex=True)
    plt.style.use("seaborn-v0_8-whitegrid")

    # Position vs time
    ax1.plot(time_points, positions, label="Drone Position", color="blue", linewidth=2)
    ax1.axhline(y=desired_pos, color="red", linestyle="--", label="Desired Position")
    ax1.set_ylabel("Y-Position (m)")
    ax1.set_title("Drone Position")
    ax1.legend()

    # Force vs time
    ax2.plot(
        time_points, forces, label="Total Force (P+I+D)", color="black", linewidth=2.5
    )
    ax2.plot(time_points, p_comps, label="Proportional (P)", linestyle=":")
    ax2.plot(time_points, i_comps, label="Integral (I)", linestyle=":")
    ax2.plot(time_points, d_comps, label="Derivative (D)", linestyle=":")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Force (N)")
    ax2.set_title("PID Force Components Over Time")
    ax2.legend()

    plt.tight_layout()
    return fig
