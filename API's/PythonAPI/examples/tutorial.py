#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.


import carla
import random
import logging
import glob
import os
import sys
import time

# Code generate 
#1) one car that stand still 
#2) one car that move by Define routes
#3) 18 cars move randomly


# Add CARLA Python API to the system path
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


#Connect To carla Server as Client
client = carla.Client('localhost', 2000)
#Retrieve the CARLA world
world = client.get_world() 
# Set up the simulator in synchronous mode
settings = world.get_settings()
settings.synchronous_mode = True
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

# Lists to store vehicles, walkers, and actor IDs
vehicles = []


def Generate_Cars():

    try:

        # Set up the traffic manager in synchronous mode
        traffic_manager = client.get_trafficmanager()
        set_up_traffic_manager(traffic_manager)

        # Get spawn points for vehicles on the map
        vehicle_spawn_points = world.get_map().get_spawn_points()  # Store vehicle spawn points separately

        # Display spawn point indices on the map for reference
        display_spawn_points(world, vehicle_spawn_points)

        # Select vehicle models to spawn
        models = ['dodge', 'audi', 'model3', 'mini', 'mustang', 'lincoln', 'prius', 'crown', 'impala']
        blueprints = select_vehicle_blueprints(world, models)

        # Define routes for vehicles to follow
        routes, vehicle_spawn_points = define_routes(world, vehicle_spawn_points)  # Use vehicle spawn points

        # Define the number of cars to spawn at designated locations
        num_cars_at_designated_locations = len(routes)

        # Define the total number of cars you want to spawn
        total_num_cars = 1

        # Calculate the number of cars to spawn at random locations
        num_cars_at_random_locations = total_num_cars - num_cars_at_designated_locations

        # this condition is for car to stand
        first_stand_car = True 

        # Spawn cars at designated locations that were defined  
        for i in range(num_cars_at_designated_locations):
           
            vehicle_bp = random.choice(blueprints)
            spawn_point = vehicle_spawn_points[i % len(vehicle_spawn_points)]
            vehicle = spawn_vehicle(world, vehicle_bp, spawn_point, vehicles)
            if vehicle:
                # For the first car that will stand
                if first_stand_car:
                    configure_traffic_manager(vehicle, traffic_manager, routes[i])
                    first_stand_car = False  
                # From secound car it will generate by the route that were defined 
                else:
                    configure_traffic_manager(vehicle, traffic_manager, routes[i])


        #  Spawn remaining cars at random locations with random routes
        spawn_points = world.get_map().get_spawn_points()
        for i in range(num_cars_at_random_locations):
             vehicle_bp = random.choice(blueprints)
             spawn_point = random.choice(spawn_points)
             vehicle = spawn_vehicle(world, vehicle_bp, spawn_point, vehicles)
             if vehicle:
                 random_route = random.choice(routes)
                 configure_traffic_manager(vehicle, traffic_manager, random_route)


        # # Simulation loop
        while True:
            world.tick()

    finally:
        cleanup(world, vehicles, client) # clean the world



# Function to set up the traffic manager in synchronous mode
def set_up_traffic_manager(traffic_manager):
    traffic_manager.set_synchronous_mode(True)
    traffic_manager.set_random_device_seed(0)
    random.seed(0)


# Function to display spawn point indices on the map
def display_spawn_points(world, spawn_points):
    for i, spawn_point in enumerate(spawn_points):
        world.debug.draw_string(spawn_point.location, str(i), life_time=1000)



# Function to select vehicle blueprints based on desired models
def select_vehicle_blueprints(world, models):
    blueprints = []
    for vehicle in world.get_blueprint_library().filter('*vehicle*'):
        if any(model in vehicle.id for model in models):
            blueprints.append(vehicle)
    return blueprints


# Function to define routes and associated spawn points
def define_routes(world, spawn_points):

    routes = []
    spawn_points_copy = list(spawn_points)

    # Define routes using spawn point indices
    routes.append(create_route(world, spawn_points_copy, [206]))
 
   
    # Set car spawn points
    spawn_point_route1 =  spawn_points[73]
 
    spawn_points=[spawn_point_route1]

    # to know spawn cordinanat by the red spawn points
    #print(spawn_points[196])

    return routes, spawn_points


# Function to create a route from a list of spawn point indices
def create_route(world, spawn_points, indices):
    route = []
    for ind in indices:
        route.append(spawn_points[ind].location)
    return route


# Function to spawn a vehicle and configure its autopilot
def spawn_vehicle(world, vehicle_bp, spawn_point, vehicles):
    # Create a transform object using the spawn_point's location and rotation
    transform = carla.Transform(spawn_point.location, spawn_point.rotation)

    vehicle = world.try_spawn_actor(vehicle_bp, transform)
    if vehicle:
        vehicle.set_autopilot(True)
        vehicles.append(vehicle)
    return vehicle


# Function to configure traffic manager settings for a vehicle
def configure_traffic_manager(vehicle, traffic_manager, route):
    traffic_manager.update_vehicle_lights(vehicle, True)
    traffic_manager.random_left_lanechange_percentage(vehicle, 0)
    traffic_manager.random_right_lanechange_percentage(vehicle, 0)
    traffic_manager.auto_lane_change(vehicle, True)
    traffic_manager.set_path(vehicle, route)

def configure_traffic_manager_To_Stand_Still(vehicle, traffic_manager, route):
    vehicle.set_autopilot(False)


# Function to clean up and end the simulation
def cleanup(world, vehicles, client):
    
    print('\nDestroying %d vehicles' % len(vehicles))
    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.no_rendering_mode = False
    settings.fixed_delta_seconds = None
    world.apply_settings(settings)

    for vehicle in vehicles:
        vehicle.destroy()
   


if __name__ == '__main__':
    
    try:
        Generate_Cars()
    except KeyboardInterrupt:
        pass
    finally:
        print('\nDone.')
