import numpy as np
import matplotlib.pyplot as plt


class Plotter:
    def __init__(
        self,
        time_points,
        drone_path,
        forces,
        p_components,
        i_components,
        d_components,
        desired_pos,
    ):
        self.time_points = time_points
        self.drone_path = drone_path
        self.forces = forces
        self.p_components = p_components
        self.i_components = i_components
        self.d_components = d_components
        self.desired_pos = desired_pos
        self.number_dimensions = self.drone_path.shape[1]

    def plot_drone_path(self, output_filename: str = None):
        if self.number_dimensions not in [2, 3]:
            return

        # Prepare data for 3D plotting
        if self.number_dimensions == 2:
            # Add a Z-axis of zeros to the 2D data
            z_zeros = np.zeros((self.drone_path.shape[0], 1))
            positions_3d = np.hstack((self.drone_path, z_zeros))
            desired_pos_3d = np.append(self.desired_pos, 0)
        else:
            positions_3d = self.drone_path[:, :3]
            desired_pos_3d = self.desired_pos[:3]

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

        if output_filename:
            plt.savefig(output_filename)

        return fig

    def plot_charts(self, output_filename: str = None):
        fig, axes = plt.subplots(
            self.number_dimensions,
            2,
            figsize=(12, 4 * self.number_dimensions),
            sharex=True,
            squeeze=False,
        )
        plt.style.use("seaborn-v0_8-whitegrid")
        dim_labels = ["X", "Y", "Z"]

        for i in range(self.number_dimensions):
            ax1 = axes[i, 0]
            ax2 = axes[i, 1]
            dim_label = dim_labels[i] if i < len(dim_labels) else f"Dim {i+1}"

            # Position vs time
            pos_data = self.drone_path[:, i]
            ax1.plot(
                self.time_points,
                pos_data,
                label="Drone Position",
                color="blue",
                linewidth=2,
            )
            ax1.axhline(
                y=self.desired_pos[i],
                color="red",
                linestyle="--",
                label="Desired Position",
            )
            ax1.set_ylabel(f"{dim_label}-Position (m)")
            ax1.set_title(f"Drone Position ({dim_label})")
            ax1.legend()

            # Force vs time
            ax2.plot(
                self.time_points,
                self.forces[:, i],
                label="Total Force (P+I+D)",
                color="black",
                linewidth=2.5,
            )
            ax2.plot(
                self.time_points,
                self.p_components[:, i],
                label="Proportional (P)",
                linestyle=":",
            )
            ax2.plot(
                self.time_points,
                self.i_components[:, i],
                label="Integral (I)",
                linestyle=":",
            )
            ax2.plot(
                self.time_points,
                self.d_components[:, i],
                label="Derivative (D)",
                linestyle=":",
            )
            ax2.set_ylabel("Force (N)")
            ax2.set_title(f"PID Force Components ({dim_label})")
            ax2.legend()

        axes[-1, 0].set_xlabel("Time (s)")
        axes[-1, 1].set_xlabel("Time (s)")

        plt.tight_layout()
        if output_filename:
            plt.savefig(output_filename)

        return fig
