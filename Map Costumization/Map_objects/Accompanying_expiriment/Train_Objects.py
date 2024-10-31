import carla
import random
import time

# ==== Settings ====
# Connect to CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)  # Timeout in seconds
tm = client.get_trafficmanager()
tm_port = tm.get_port()

# Set traffic manager parameters
tm.set_global_distance_to_leading_vehicle(2.0)  # Global distance to leading vehicle
tm.set_synchronous_mode(True)  # Synchronous mode for better control
tm.set_random_device_seed(0)  # Seed for reproducibility
tm.global_percentage_speed_difference(-10)  # Slow down traffic slightly

# Create an empty list to hold the spawned vehicles
vehicles = []

def get_random_spawn_point():
    """Get a random spawn point from the available spawn points in the map."""
    spawn_points = world.get_map().get_spawn_points()
    return random.choice(spawn_points)

def try_spawn_vehicle(vehicle_bp, spawn_point):
    """Try to spawn a vehicle at the given spawn point. Retry if collision occurs."""
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            vehicle = world.spawn_actor(vehicle_bp, spawn_point)
            return vehicle
        except RuntimeError as e:
            if "collision" in str(e):
                spawn_point = get_random_spawn_point()
            else:
                raise e
    return None

try:
    # Retrieve world
    world = client.get_world()
    
    # Ensure the world is in synchronous mode
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    for i in range(6):
        # Get random spawn point from the map
        spawn_point = get_random_spawn_point()

        # Choose a vehicle blueprint based on the iteration
        if i == 1 or i == 4:
            vehicle_bp = random.choice(world.get_blueprint_library().filter('vehicle.citroen.c3'))
        elif i == 2 or i == 3:
            vehicle_bp = random.choice(world.get_blueprint_library().filter('vehicle.nissan.patrol'))
        else:
            vehicle_bp = random.choice(world.get_blueprint_library().filter('vehicle.ford.crown'))

        # Try to spawn the vehicle at the random spawn point
        vehicle = try_spawn_vehicle(vehicle_bp, spawn_point)

        if vehicle is not None:
            # Enable autopilot and set traffic manager settings
            vehicle.set_autopilot(True, tm_port)
            tm.auto_lane_change(vehicle, True)
            tm.distance_to_leading_vehicle(vehicle, 2.0)
            tm.vehicle_percentage_speed_difference(vehicle, random.uniform(-30, 10))  # Random speed variance

            # Add vehicle to the list
            vehicles.append(vehicle)

        time.sleep(0.5)

    # Main loop
    while True:
        world.tick()
        time.sleep(0.05)

finally:
    # Destroy all spawned actors
    for vehicle in vehicles:
        vehicle.destroy()
    print("All vehicles destroyed.")

