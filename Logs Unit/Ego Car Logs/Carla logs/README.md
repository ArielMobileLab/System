Simulation Data Documentation (output from Ego_Car_log.py and Objects_log.py codes)

This document provides documentation for the JSON data obtained from a simulation.

1. Ego car JSON:

The JSON data consists of logs containing information about GPS coordinates, orientation, speed, acceleration, and other relevant details for a simulated vehicle from Ego_Car_log.py.

## JSON Structure

The JSON structure includes the following fields:

- **Logs**: An array containing individual log entries.
  - **Type**: Type of log entry, which could be "GPS" or "CarTelemetries".
  - **WorldTime**: Time in the simulated world.
  - **SimulationTime**: Time elapsed in the simulation.
  - **FrameID**: ID of the frame.
  - **For GPS Logs**:
    - **SimulationPosition**: Coordinates (x, y, z) of the simulated object.
    - **Latitude**: Latitude coordinate.
    - **Longitude**: Longitude coordinate.
    - **Altitude**: Altitude coordinate.
    - **Orientation**: Orientation (x, y, z) of the simulated object.
    - **Speed**: Speed of the simulated object.
    - **Acceleration**: Acceleration (x, y, z) of the simulated object.
    - **VelocityLocal3D**: Local velocity (x, y, z) of the simulated object.
    - **AngularAccelerationLocal3D**: Local angular acceleration (x, y, z) of the simulated object.
  - **For CarTelemetries Logs**:
    - **Speed**: Speed of the car.
    - **Acceleration**: Acceleration of the car.
    - **SteeringAngle**: Angle of the steering.
    - **Brake**: Brake status.
    - **Gas**: Gas pedal status.
    - **Gear**: Gear position.

## Example Data

```json
{
  "Logs": [
    {
      "Type": "GPS",
      "WorldTime": "12:08:19.087489",
      "SimulationTime": 3.3666668422539208,
      "FrameID": 1,
      "SimulationPosition": {"y": 0.0, "x": 0.0, "z": 0.0},
      "Latitude": -0.001987312664070373,
      "Longitude": 0.004681669367991267,
      "Altitude": 1.9808076620101929,
      "Orientation": {"y": 0.0, "x": 0.0, "z": 0.0},
      "Speed": 0.0,
      "Acceleration": {"y": 0.0, "x": 0.0, "z": 0.0},
      "VelocityLocal3D": {"y": 0.0, "x": 0.0, "z": 0.0},
      "AngularAccelerationLocal3D": {"y": 0.0, "x": 0.0, "z": 0.0}
    },
    {
      "Type": "CarTelemetries",
      "WorldTime": "12:08:19.087489",
      "SimulationTime": 3.3666668422539208,
      "FrameID": 2,
      "Speed": -3.0157722719081906e-08,
      "Acceleration": 0.0,
      "SteeringAngle": -0.0,
      "Brake": 1.0,
      "Gas": 1.8250579833984375,
      "Gear": 1
    }
  ]
}


2. Objects JSON

The JSON data consists of logs containing information about GPS coordinates, orientation, speed, acceleration, and other relevant details for pedestrians, vehicles, and static objects in the simulated environment that we generated from Objects_log.py.

## JSON Structure

The JSON structure includes the following fields:

- **Type**: Type of log entry, which could be "GPS".
- **Name**: Name of the entity (pedestrian or vehicle).
- **WorldTime**: Time in the simulated world.
- **SimulationTime**: Time elapsed in the simulation.
- **FrameID**: ID of the frame.
- **SimulationPosition**: Coordinates (x, y, z) of the simulated object.
- **Longitude**: Longitude coordinate.
- **Latitude**: Latitude coordinate.
- **Altitude**: Altitude coordinate.
## extra fields from Dynamic objects
- **Orientation**: Orientation (x, y, z) of the simulated object.
- **Speed**: Speed of the simulated object (if applicable).
- **Acceleration**: Acceleration (x, y, z) of the simulated object (if applicable).

## Example Data

```json
{
  "Logs": [
    {
      "Type": "GPS",
      "Name": "walker.pedestrian.0002 239",
      "WorldTime": "12:08:50.139295",
      "SimulationTime": 28.40000148119149,
      "FrameID": 152,
      "SimulationPosition": {"y": 8.09597969055, "x": 93.8221206665, "z": 0.951499998569},
      "Longitude": 0.00261394629658,
      "Latitude": -0.00155842610833,
      "Altitude": 0.951499998569
    },
    {
      "Type": "GPS",
      "Name": "vehicle.tesla.model3 240",
      "WorldTime": "12:08:50.175701",
      "SimulationTime": 28.43333481626331,
      "FrameID": 153,
      "SimulationPosition": {"y": -1.22453606129, "x": 334.511779785, "z": 0.00163711549249},
      "Orientation": {"y": -179.547851562, "x": 0.00700777349994, "z": -0.000335693301167},
      "Longitude": 0.00477609829247,
      "Latitude": -0.0014746984908,
      "Altitude": 0.00163711549249,
      "Speed": 3.292794007242734,
      "Acceleration": {"y": -0.00683765858412, "x": -0.254273414612, "z": 3.81469726562e-06}
    },
    // More data entries
  ]
}
