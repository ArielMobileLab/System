Lane Centering using Pure Pursuit Controller
This version works 

Refference : https://github.com/reachpranjal/pure-pursuit-carla

Notes about the version:

- The code works in Carla simulation only, an adaptation must be made in the future that will be modular for all types of simulators
- there is two versions
  1. Pure_pursit_automatic_waypoints - Enter a bank of points and the vehicle will follow them
  2. Give a location on the map of the ego car and the code alone will create the closest points through the waypoints closest to it
