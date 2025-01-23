This is the project for the "Smart Systems for Data Acquisition" Exam.

The project is based on a simple electronic circuit composed by 2 hall-effect sensors that must detect the arriving direction of a drone. To do so the drone has a permanent magnet installed on it.
The sensors are located with a 90° displacement among each other and titled 45° with respect to ground; a 3D-printed base has been used to fix their respective positions. 
In order to acquire the signals, an OPAMP based circuit has been built, using a differential amplifier configuration. 
For the acquisition of data, the ADS7038Q1EVM-PDK Texas Instrument Analog to Digital Converter has been adopted, using its generated CSV in this Python script to extract information.
Specifically data from each sensor have been processed in order to have a useable value and compared to determine if a drone is passing over one or both sensor and even to evaluate the 2D-direction (parallel to ground).
Directions that can be detected are 0° (only Sensor 2 detects the drone), 30°, 45°, 60° and 90° (only Sensor 1 detects the drone). 
