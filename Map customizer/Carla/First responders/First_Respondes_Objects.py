import carla
import random
import time

# Connect to CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)  # Timeout in seconds

# Create an empty list to hold the spawned vehicles
vehicles = []

try:
    # Retrieve world
    world = client.get_world()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
    # Define the target coordinates and rotation for the first vehicle (Firetruck)
    target_location_firetruck = carla.Location(x=-150.918556, y=15.8, z=10.003113)
    target_rotation_firetruck = carla.Rotation(pitch=-1.156556, yaw=-130, roll=0.0)
    spawn_transform_firetruck = carla.Transform(target_location_firetruck, target_rotation_firetruck)

    # Choose a Firetruck blueprint
    firetruck_bp = random.choice(world.get_blueprint_library().filter('vehicle.carlamotors.firetruck'))

    # Spawn the Firetruck at the specified location and rotation
    firetruck = world.spawn_actor(firetruck_bp, spawn_transform_firetruck)
    firetruck.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, brake=1.0))
    vehicles.append(firetruck)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
    # Define the target coordinates and rotation for the second vehicle (Tesla Model 3)
    Carsh_Car_Place = carla.Location(x=-160.918556, y=15.0, z=10.003113)
    Carsh_Car_Rotate = carla.Rotation(pitch=150, yaw=0.0, roll=0.0)
    Carsh_Car_Swap = carla.Transform(Carsh_Car_Place, Carsh_Car_Rotate)

    # Choose a Tesla Model 3 blueprint
    tesla_bp = random.choice(world.get_blueprint_library().filter('vehicle.tesla.model3'))

    # Spawn the Tesla Model 3 at the specified location and rotation
    Carsh_Car = world.spawn_actor(tesla_bp, Carsh_Car_Swap)
    Carsh_Car.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, brake=1.0))
    vehicles.append(Carsh_Car)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
 # Define the target coordinates and rotation for the second vehicle (Tesla Model 3)
    x1_place = carla.Location(x=-170.918556, y=9.2, z=10.003113)
    x1_rotate = carla.Rotation(pitch=-1.156556, yaw=-179.923187, roll=0.0)
    x1_swap = carla.Transform(x1_place, x1_rotate)

    # Choose a Tesla Model 3 blueprint
    tesla_bp = random.choice(world.get_blueprint_library().filter('vehicle.tesla.model3'))

    # Spawn the Tesla Model 3 at the specified location and rotation
    x1 = world.spawn_actor(tesla_bp, x1_swap)
    x1.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, brake=1.0))
    vehicles.append(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
 # Define the target coordinates and rotation for the second vehicle (Tesla Model 3)
    x2_place = carla.Location(x=-160.918556, y=9.2, z=10.003113)
    x2_rotate = carla.Rotation(pitch=-1.156556, yaw=-179.923187, roll=0.0)
    x2_swap = carla.Transform(x2_place, x2_rotate)

    # Choose a Tesla Model 3 blueprint
    tesla_bp = random.choice(world.get_blueprint_library().filter('vehicle.tesla.model3'))

    # Spawn the Tesla Model 3 at the specified location and rotation
    x2 = world.spawn_actor(tesla_bp, x2_swap)
    x2.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, brake=1.0))
    vehicles.append(x2)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

    Gap_Cars_place = carla.Location(x=0.0, y=6.5, z=15.0)
    Gap_Cars_rotate = carla.Rotation(pitch=-1.156556, yaw=-179.923187, roll=0.0)
    Gap_Cars_swap = carla.Transform(Gap_Cars_place, Gap_Cars_rotate)
  


    # Spawn the vehicles
    for i in range(5):
            random_bp = random.choice(world.get_blueprint_library().filter('vehicle.tesla.model3'))

            Gap_size = 3.5
         

            Gap_Cars = world.spawn_actor(random_bp, Gap_Cars_swap)
            Gap_Cars.apply_control(carla.VehicleControl(throttle=0.2, steer=0.0))

            vehicles.append(Gap_Cars)

            time.sleep(Gap_size)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    traffic_manager = client.get_trafficmanager()
    traffic_manager.set_synchronous_mode(False)
    traffic_manager.set_random_device_seed(0)
    traffic_manager.set_global_distance_to_leading_vehicle(15.0)
    random.seed(0)


    # Define the target coordinates and rotation for the ambulance
    ambulance_place = carla.Location(x=-15.0, y=9.2, z=15.0)
    ambulance_rotate = carla.Rotation(pitch=-1.156556, yaw=-179.923187, roll=0.0)
    ambulance_transform = carla.Transform(ambulance_place, ambulance_rotate)
    # Choose an ambulance blueprint
    ambulance_bp = random.choice(world.get_blueprint_library().filter('vehicle.ford.ambulance'))

    # Spawn the ambulance at the specified location and rotation
    ambulance = world.spawn_actor(ambulance_bp, ambulance_transform)
     
    # Enable headlights for better visibility
    ambulance.set_autopilot(True)
    # Set lane change parameters
    traffic_manager.update_vehicle_lights(ambulance, True)
    traffic_manager.random_left_lanechange_percentage(ambulance, 0)
    traffic_manager.random_right_lanechange_percentage(ambulance, 0)
    traffic_manager.auto_lane_change(ambulance, True)
    traffic_manager.vehicle_percentage_speed_difference(ambulance,-50)

    #traffic_manager.random_left_lanechange_percentage(ambulance, 50)
    #traffic_manager.random_right_lanechange_percentage(ambulance, 50)
    #traffic_manager.auto_lane_change(ambulance, True)
    # Define a random route for the ambulance (list of waypoints)
    #route = [destination_waypoint]
    #
    #  Set the random path for the ambulance
    #traffic_manager.set_path(ambulance, route, False)  # Setting empty_buffer=False
    
    vehicles.append(ambulance)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!!!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``

    Gap_Cars_place = carla.Location(x=-0.0, y=6.5, z=15.0)
    Gap_Cars_rotate = carla.Rotation(pitch=-1.156556, yaw=-179.923187, roll=0.0)
    Gap_Cars_swap = carla.Transform(Gap_Cars_place, Gap_Cars_rotate)
  


    # Spawn the vehicles
    for i in range(10):
            random_bp = random.choice(world.get_blueprint_library().filter('vehicle.tesla.model3'))

            Gap_size = 3.5
         

            Gap_Cars = world.spawn_actor(random_bp, Gap_Cars_swap)
            Gap_Cars.apply_control(carla.VehicleControl(throttle=0.2, steer=0.0))

            vehicles.append(Gap_Cars)

            time.sleep(Gap_size)
    
    # Wait for a few seconds

finally:
    # Destroy all spawned actors
    for vehicle in vehicles:
        vehicle.destroy()

