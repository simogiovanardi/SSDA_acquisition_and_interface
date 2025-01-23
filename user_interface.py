import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class RadarDirectionVisualizer:
    def __init__(self, root, angles):
        self.root = root
        self.angles = np.deg2rad(angles)  # Convert input angles from degrees to radians
        self.colors = ['red', 'grey', 'blue', 'orange', 'purple', 'yellow']  # Color pool
        self.current_index = 0  # Track which angle is currently being plotted

        # Set up the main frame
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Create the radar chart
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))
        self.ax.set_ylim(0, 1)
        self.ax.set_yticks([])  # Remove the radial grid lines

        # Set up xticks and mirrored, rotated labels
        original_ticks = np.arange(0, 360, 45)
        mirrored_ticks = (360 - original_ticks) % 360
        rotated_labels = (mirrored_ticks + 180) % 360
        self.ax.set_xticks(np.deg2rad(original_ticks))
        self.ax.set_xticklabels([f"{int(tick)}°" for tick in rotated_labels])

        # Prepare the canvas to render the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # Add buttons to plot the next and previous angles
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack()

        self.prev_button = tk.Button(self.button_frame, text="PLOT PREVIOUS ANGLE", command=self.plot_previous_angle)
        self.prev_button.pack(side=tk.LEFT)  # Place the button on the left

        self.next_button = tk.Button(self.button_frame, text="PLOT NEXT ANGLE", command=self.plot_next_angle)
        self.next_button.pack(side=tk.LEFT)  # Place the button on the right

        # Initially disable the "PLOT PREVIOUS ANGLE" button
        self.update_buttons()

        # Plot the first angle on initialization
        self.update_plot()

        # Override the close button behavior to clean up properly
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Handle the behavior when the user closes the window."""
        self.root.destroy()  # Destroy the Tkinter root window
        plt.close('all')     # Close all Matplotlib figures (if any remain open)

    def plot_next_angle(self):
        """Move to the next angle and update the plot."""
        if self.current_index < len(self.angles) - 1:  # Ensure we're not past the last angle
            self.current_index += 1  # Move to the next angle
            self.update_plot()       # Update the plot
        self.update_buttons()        # Update button states

    def plot_previous_angle(self):
        """Move to the previous angle and update the plot."""
        if self.current_index > 0:  # Ensure we're not before the first angle
            self.current_index -= 1  # Move to the previous angle
            self.update_plot()       # Update the plot
        self.update_buttons()        # Update button states

    def update_plot(self):
        """Clear the plot and visualize the current angle."""
        # Clear previous plot
        self.ax.cla()

        # Restore xticks and labels (since cla() removes them)
        self.restore_chart_settings()

        # Get the current angle
        angle = self.angles[self.current_index]
        color = self.colors[self.current_index % len(self.colors)]  # Cycle colors if not enough

        # Apply mirroring and 180° rotation
        mirrored_angle = -angle  # Mirror the angle around the y-axis
        rotated_angle = (mirrored_angle + np.pi) % (2 * np.pi)  # Rotate the mirrored angle by 180°

        # Add the sector to the plot
        self.add_sector(self.ax, rotated_angle, self.current_index + 1, color)

        # Redraw the canvas with the updated plot
        self.canvas.draw()

    def restore_chart_settings(self):
        """Restore xticks, labels, and chart settings after clearing the plot."""
        original_ticks = np.arange(0, 360, 45)
        mirrored_ticks = (360 - original_ticks) % 360
        rotated_labels = (mirrored_ticks + 180) % 360
        self.ax.set_xticks(np.deg2rad(original_ticks))
        self.ax.set_xticklabels([f"{int(tick)}°" for tick in rotated_labels])
        self.ax.set_ylim(0, 1)
        self.ax.set_yticks([])  # Remove radial grid lines

    def add_sector(self, ax, center_angle, label_index, color):
        # Calculate start and end angles for the 5° sector
        start_angle = center_angle - np.deg2rad(8)
        end_angle = center_angle + np.deg2rad(8)

        # Add a wedge (sector) highlighting the segment
        ax.fill_between(
            [start_angle, end_angle],
            0, 1,
            color=color,  # Assign the color dynamically
            alpha=0.5
        )

        # Add a label for the sector
        # Place the fixed label in the upper-left corner of the plot
        ax.text(
            -0.1, 1.05,  # Fixed position in Cartesian coordinates (upper left)
            f"ARRIVING DIRECTION: \n          {label_index} out of {len(self.angles)}",  # Dynamic label
            fontsize=12,
            color='black',  # Match label color to the sector's color
            ha='left',  # Align the text to the left
            va='top',   # Align the text vertically at the top
            transform=ax.transAxes  # Use Axes coordinates for positioning
        )

    def update_buttons(self):
        """Enable or disable buttons based on current index."""
        if self.current_index == 0:
            self.prev_button['state'] = 'disabled'  # Disable if at the first angle
        else:
            self.prev_button['state'] = 'normal'

        if self.current_index == len(self.angles) - 1:
            self.next_button['state'] = 'disabled'  # Disable if at the last angle
        else:
            self.next_button['state'] = 'normal'