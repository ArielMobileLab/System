import carla
import time
import random

# Connect to CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)  # Timeout in seconds
world = client.get_world()



def display_spawn_points(world, spawn_points):
    for i, spawn_point in enumerate(spawn_points):
        world.debug.draw_string(spawn_point.location, str(i), life_time=1000)
    spawn_point_158 = vehicle_spawn_points[158]
    print("Coordinates of spawn point 158:")
    print("X:", spawn_point_158.location.x)
    print("Y:", spawn_point_158.location.y)
    print("Z:", spawn_point_158.location.z)


    
vehicle_spawn_points = world.get_map().get_spawn_points()

display_spawn_points(world, vehicle_spawn_points)

