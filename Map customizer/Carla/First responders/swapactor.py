import carla
import random
import time

# Connect to CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)  # Timeout in seconds

vehicles = []  # Define vehicles list outside the try block

try:
    # Retrieve world
    world = client.get_world()

    # Choose a vehicle blueprint
    vehicle_bp = random.choice(world.get_blueprint_library().filter('vehicle.*'))

    # Choose spawn points
    spawn_points = random.sample(world.get_map().get_spawn_points(), k=100)

    # Spawn the vehicles
    for spawn_point in spawn_points:
        print(spawn_point)
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
        vehicles.append(vehicle)
	time.sleep(0.75)
    # Wait for a few seconds
    time.sleep(5)

finally:
    # Destroy the spawned actors
    for vehicle in vehicles:
        vehicle.destroy()

