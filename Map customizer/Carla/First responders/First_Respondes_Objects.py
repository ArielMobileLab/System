import carla
import random
import time

# ==== Settings ====
# Connect to CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)  # Timeout in seconds
tm = client.get_trafficmanager()
tm_port = tm.get_port()

# ==== Cars Types ====
vehicle_types = [
    "vehicle.ford.crown", 
    "vehicle.ford.mustang", 
    "vehicle.lincoln.mkz_2017", 
    "vehicle.lincoln.mkz_2020", 
    "vehicle.mercedes.coupe", 
    "vehicle.nissan.patrol", 
    "vehicle.nissan.patrol_2021", 
    "vehicle.seat.leon", 
    "vehicle.mercedes.coupe", 
    "vehicle.toyota.prius", 
    "vehicle.tesla.cybertruck", 
    "vehicle.mercedes.coupe", 
    "vehicle.mercedes.sprinter", 
    "vehicle.dodge.charger_2020", 
    "vehicle.chevrolet.impala", 
    "vehicle.audi.tt"
]


def get_available_car_models():
    global world
    models = ['dodge', 'audi', 'model3', 'mini', 'mustang', 'lincoln', 'prius', 'nissan', 'crown', 'impala']
    blueprints = []
    for vehicle in world.get_blueprint_library().filter('*vehicle*'):
        if any(model in vehicle.id for model in models):
            blueprints.append(vehicle)
    return blueprints

# Create an empty list to hold the spawned vehicles
vehicles = []

try:
    # Retrieve world
    world = client.get_world()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
    # Define the target coordinates and rotation for the first vehicle (Firetruck)
    target_location_firetruck = carla.Location(x=-505, y=140.0, z=10.003113)
    target_rotation_firetruck = carla.Rotation(pitch=-1.156556, yaw=-250, roll=0.0)
    spawn_transform_firetruck = carla.Transform(target_location_firetruck, target_rotation_firetruck)

    # Choose a Firetruck blueprint
    firetruck_bp = random.choice(world.get_blueprint_library().filter('vehicle.carlamotors.firetruck'))

    # Spawn the Firetruck at the specified location and rotation
    firetruck = world.spawn_actor(firetruck_bp, spawn_transform_firetruck)
    firetruck.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, brake=1.0))
    vehicles.append(firetruck)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
    # Define the target coordinates and rotation for the second vehicle (Tesla Model 3)
    Carsh_Car_Place = carla.Location(x=-505, y=150.0, z=5.0)
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
    x1_place = carla.Location(x=-510, y=145, z=5.0)
    x1_rotate = carla.Rotation(pitch=-1.156556, yaw=90.0, roll=0.0)
    x1_swap = carla.Transform(x1_place, x1_rotate)

    # Choose a Tesla Model 3 blueprint
    tesla_bp = random.choice(world.get_blueprint_library().filter('vehicle.tesla.model3'))

    # Spawn the Tesla Model 3 at the specified location and rotation
    x1 = world.spawn_actor(tesla_bp, x1_swap)
    x1.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, brake=1.0))
    vehicles.append(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
 # Define the target coordinates and rotation for the second vehicle (Tesla Model 3)
    x2_place = carla.Location(x=-510, y=152, z=5.0)
    x2_rotate = carla.Rotation(pitch=-1.156556, yaw=90.0, roll=0.0)
    x2_swap = carla.Transform(x2_place, x2_rotate)

    # Choose a Tesla Model 3 blueprint
    tesla_bp = random.choice(world.get_blueprint_library().filter('vehicle.tesla.model3'))

    # Spawn the Tesla Model 3 at the specified location and rotation
    x2 = world.spawn_actor(tesla_bp, x2_swap)
    x2.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, brake=1.0))
    vehicles.append(x2)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
    spawn_points = world.get_map().get_spawn_points()
    start_point = spawn_points[181]
    start_point.location.x = -400
    start_point.location.y = 6.5
    start_point.location.z = 5.0
    start_point.rotation.yaw = -179.923187


    for i in range(20):
        if i == 6:
            ambulance_place = carla.Location(x=-400, y=10.0, z=5.0)
            ambulance_rotate = carla.Rotation(pitch=-1.156556, yaw=-179.923187, roll=0.0)
            ambulance_transform = carla.Transform(ambulance_place, ambulance_rotate)
            # Choose an ambulance blueprint
            ambulance_bp = random.choice(world.get_blueprint_library().filter('vehicle.ford.ambulance'))

            # Spawn the ambulance at the specified location and rotation
            ambulance = world.spawn_actor(ambulance_bp, ambulance_transform)

            # Enable headlights for better visibility
            ambulance.set_autopilot(True)
            # Set lane change parameters
            tm.update_vehicle_lights(ambulance, True)
            tm.random_left_lanechange_percentage(ambulance, 0)
            tm.random_right_lanechange_percentage(ambulance, 0)
            tm.auto_lane_change(ambulance, True)
            tm.vehicle_percentage_speed_difference(ambulance,10)
            tm.set_global_distance_to_leading_vehicle(15.0) 
            vehicles.append(ambulance)
            time.sleep(1)
        if i == 8:   
            

        else:
            print(i)
            car_type = random.choice(vehicle_types)
            car_bp = random.choice(world.get_blueprint_library().filter('vehicle.mercedes.sprinter'))
            vehicle = world.try_spawn_actor(car_bp, start_point)
            vehicle.set_autopilot(True) 
            tm.auto_lane_change(vehicle,False)
            vehicles.append(vehicle)
            time.sleep(5)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

    # # Define the target coordinates and rotation for the ambulance
    # ambulance_place = carla.Location(x=-400, y=10.0, z=5.0)
    # ambulance_rotate = carla.Rotation(pitch=-1.156556, yaw=-179.923187, roll=0.0)
    # ambulance_transform = carla.Transform(ambulance_place, ambulance_rotate)
    # # Choose an ambulance blueprint
    # ambulance_bp = random.choice(world.get_blueprint_library().filter('vehicle.ford.ambulance'))

    # # Spawn the ambulance at the specified location and rotation
    # ambulance = world.spawn_actor(ambulance_bp, ambulance_transform)
     
    # # Enable headlights for better visibility
    # ambulance.set_autopilot(True)
    # # Set lane change parameters
    # tm.update_vehicle_lights(ambulance, True)
    # tm.random_left_lanechange_percentage(ambulance, 0)
    # tm.random_right_lanechange_percentage(ambulance, 0)
    # tm.auto_lane_change(ambulance, True)
    # tm.vehicle_percentage_speed_difference(ambulance,10)
    # tm.set_global_distance_to_leading_vehicle(15.0)

    # #traffic_manager.random_left_lanechange_percentage(ambulance, 50)
    # #traffic_manager.random_right_lanechange_percentage(ambulance, 50)
    # #traffic_manager.auto_lane_change(ambulance, True)
    # # Define a random route for the ambulance (list of waypoints)
    # #route = [destination_waypoint]
    # #
    # #  Set the random path for the ambulance
    # #traffic_manager.set_path(ambulance, route, False)  # Setting empty_buffer=False
    
    # vehicles.append(ambulance)

#     Gap_Cars_place = carla.Location(x=30.0, y=6.5, z=15.0)
#     Gap_Cars_rotate = carla.Rotation(pitch=-1.156556, yaw=-179.923187, roll=0.0)
#     Gap_Cars_swap = carla.Transform(Gap_Cars_place, Gap_Cars_rotate)
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # for i in range(3):
    #         car_type = random.choice(vehicle_types)
    #         car_bp = random.choice(world.get_blueprint_library().filter(car_type))
    #         vehicle = world.try_spawn_actor(car_bp, start_point)
    #         vehicle.set_autopilot(True) 
    #         tm.auto_lane_change(vehicle,False)
    #         vehicles.append(vehicle)
    #         time.sleep(5)


#     # Spawn the vehicles
#     for i in range(5):
#             random_bp = random.choice(world.get_blueprint_library().filter('vehicle.tesla.model3'))

#             Gap_size = 5.0
         

#             Gap_Cars = world.spawn_actor(random_bp, Gap_Cars_swap)
#             Gap_Cars.apply_control(carla.VehicleControl(throttle=0.2, steer=0.0))

#             vehicles.append(Gap_Cars)

#             time.sleep(Gap_size)
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#     traffic_manager = client.get_trafficmanager()

#     # traffic_manager = client.get_trafficmanager()
#     #traffic_manager.set_synchronous_mode(False)
#     #traffic_manager.set_random_device_seed(0)
#     #traffic_manager.set_global_distance_to_leading_vehicle(15.0)
#     #random.seed(0)


#     # Define the target coordinates and rotation for the ambulance
#     ambulance_place = carla.Location(x=0.0, y=9.2, z=15.0)
#     ambulance_rotate = carla.Rotation(pitch=-1.156556, yaw=-179.923187, roll=0.0)
#     ambulance_transform = carla.Transform(ambulance_place, ambulance_rotate)
#     # Choose an ambulance blueprint
#     ambulance_bp = random.choice(world.get_blueprint_library().filter('vehicle.ford.ambulance'))

#     # Spawn the ambulance at the specified location and rotation
#     ambulance = world.spawn_actor(ambulance_bp, ambulance_transform)
     
#     # Enable headlights for better visibility
#     ambulance.set_autopilot(True)
#     # Set lane change parameters
#     traffic_manager.update_vehicle_lights(ambulance, True)
#     traffic_manager.random_left_lanechange_percentage(ambulance, 0)
#     traffic_manager.random_right_lanechange_percentage(ambulance, 0)
#     traffic_manager.auto_lane_change(ambulance, True)
#     traffic_manager.vehicle_percentage_speed_difference(ambulance,10)

#     #traffic_manager.random_left_lanechange_percentage(ambulance, 50)
#     #traffic_manager.random_right_lanechange_percentage(ambulance, 50)
#     #traffic_manager.auto_lane_change(ambulance, True)
#     # Define a random route for the ambulance (list of waypoints)
#     #route = [destination_waypoint]
#     #
#     #  Set the random path for the ambulance
#     #traffic_manager.set_path(ambulance, route, False)  # Setting empty_buffer=False
    
#     vehicles.append(ambulance)


# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!!!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``

#     Gap_Cars_place = carla.Location(x=30.0, y=6.5, z=15.0)
#     Gap_Cars_rotate = carla.Rotation(pitch=-1.156556, yaw=-179.923187, roll=0.0)
#     Gap_Cars_swap = carla.Transform(Gap_Cars_place, Gap_Cars_rotate)
  


#     # Spawn the vehicles
#     for i in range(10):
#             random_bp = random.choice(world.get_blueprint_library().filter('vehicle.tesla.model3'))

#             Gap_size = 5.0
         

#             Gap_Cars = world.spawn_actor(random_bp, Gap_Cars_swap)
#             Gap_Cars.apply_control(carla.VehicleControl(throttle=0.2, steer=0.0))

#             vehicles.append(Gap_Cars)

#             time.sleep(Gap_size)
    
#     # Wait for a few seconds

finally:
    time.sleep(1000)
    # Destroy all spawned actors
    for vehicle in vehicles:
        vehicle.destroy()
