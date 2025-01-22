import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read data from the CSV file
data = pd.read_csv('2 sensors(forth)_very_good.csv')

# Extract columns
sensor_1 = data['CH-0'].values
sensor_2 = data['CH-1'].values

# Normalize the sensor outputs (if needed)
sensor_1 = sensor_1 / max(sensor_1)
sensor_2 = sensor_2 / max(sensor_2)


# Compute angles in degrees
angles = np.degrees(np.arctan2(sensor_2, sensor_1))
angles = np.where(angles < 0, 90 + angles, angles)


# Create a radar-style plot
plt.figure()
ax = plt.subplot(111, polar=True)

# Convert angles to radians and plot
radians = np.radians(angles)
magnitude = np.sqrt(sensor_1**2 + sensor_2**2)  # Combine magnitudes for plotting
ax.scatter(radians, magnitude, color='blue', label='Arrival Direction')

# Customize axis
ax.set_theta_zero_location('N')  # North is 0 degrees
ax.set_theta_direction(-1)       # Clockwise

plt.legend()
plt.show()


'''
### 4. **Probabilistic Pattern Evaluation**
   To evaluate patterns across multiple acquisitions:
   - Record the acquisitions over time.
   - Compute and plot the **mean direction** and **variance** for repeated measurements for each direction.
   - Use a 2D **heatmap** or a polar plot to visualize probabilities based on normalized histogram binning of the directions.
   
```python
# Aggregating and evaluating probability patterns
from scipy.stats import norm

# Example: Fit a Gaussian to the angles data
mean_angle = np.mean(angles)
std_dev = np.std(angles)

# Generate probabilities and visualize as heatmap
angles_range = np.linspace(0, 90, 100)
probabilities = norm.pdf(angles_range, mean_angle, std_dev)

plt.figure()
plt.polar(np.radians(angles_range), probabilities, label='Probabilistic Pattern')
plt.legend()
plt.show()
'''