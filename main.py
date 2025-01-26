import pandas as pd
from direction_identifier import direction_identifier
from user_interface import *

data = pd.read_csv("acquisitions/2_sensors(forth).csv") # <--- INSERT HERE THE NEW FILE




# Extract the data about the two sensors (rounding up to 3 decimal numbers)
sensor_1 = [round(value, 3) for value in data['CH-0']] # Sensor 1 ==> CH-0
sensor_2 = [round(value, 3) for value in data['CH-1']] # Sensor 2 ==> CH-1

# This is a threshold to avoid to take into account noise (mostly present in CH-0)
NOISE_THRESHOLD = 0.05

# All the events are going to be stored in this list
events = []
# This list is going to contain the actual event (drone is flying above at least one sensor) 
current_event = []


event_detected = False # used to detect the start of the event
counter = 0 # used to detect the end of the event

# Identify signal events
for a, b in zip(sensor_1, sensor_2):
   if a > NOISE_THRESHOLD or b > NOISE_THRESHOLD: 
      current_event.append((a, b)) # Add the values of the sensors to the current event
      if event_detected == False: # An event has been detected
         event_detected = True


   if event_detected == True and a < NOISE_THRESHOLD and b < NOISE_THRESHOLD:
      counter += 1

   if counter == 100: # The actual event is over (number of samples with no signals)
      if len(current_event) > 100:
         events.append(current_event)
      current_event = []
      event_detected = False
      counter = 0




# CALCULATE THE SUM OF THE VALUES OF THE SENSORS FOR EACH EVENT
sums_sensor_1 = []
sums_sensor_2 = []

for event in events:
   sums_sensor_1.append(sum(x[0] for x in event))
   sums_sensor_2.append(sum(x[1] for x in event))


# COUNT THE NUMBER OF SAMPLES FOR EACH EVENT
samples_per_event = []

for event in events:
   samples_per_event.append(len(event))

# print(f"Samples per events: {samples_per_event}")


# CALCULATE THE NORMALIZED VALUES FOR EACH EVENT
normalized_values = []

for i in range(len(events)):
   normalized_values.append((sums_sensor_1[i] / samples_per_event[i], sums_sensor_2[i] / samples_per_event[i]))
print(f"NORMALIZED VALUES: {normalized_values}")


# EVALUATION OF THE VALUES (DETECTION OF THE DRONE)
directions = []

for event in normalized_values:
   directions.append(direction_identifier(event[0], event[1]))


print(f"ANGLES EVENTS: {directions}")

# USER INTERFACE CALL
root = tk.Tk()
root.title("Drone Arrival Direction Radar")

RadarDirectionVisualizer(root, directions)
root.mainloop()


# TODO
# try to implement the fact that the script starts as soon as the file is uploaded or
# if I select the file directly from the interface


