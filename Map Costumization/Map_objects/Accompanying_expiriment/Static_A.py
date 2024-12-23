import carla


# Connect to CARLA Server as a Client
client = carla.Client('localhost', 2000)
# Retrieve the CARLA world
world = client.get_world()



    # Generate cones and cars
    # Define work zone locations (You can adjust these coordinates)
    

    # Create a traffic cone
blueprint_library = world.get_blueprint_library()



cone_car_location = carla.Location(x=270.6, y=-4, z=0.300000)
cone_car_bp = blueprint_library.filter("vehicle.ford.mustang")[0]
cone_car_transform = carla.Transform(cone_car_location, carla.Rotation(pitch=0, yaw=180, roll=0))
cone_car = world.spawn_actor(cone_car_bp, cone_car_transform)

