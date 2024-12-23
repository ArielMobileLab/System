import carla


# Connect to CARLA Server as a Client
client = carla.Client('localhost', 2000)
# Retrieve the CARLA world
world = client.get_world()



    # Generate cones and cars
    # Define work zone locations (You can adjust these coordinates)
    

    # Create a traffic cone
blueprint_library = world.get_blueprint_library()



cone_car_location = carla.Location(x=340.5, y=245, z=1.0)
cone_car_bp = blueprint_library.filter("vehicle.nissan.patrol_2021")[0]
cone_car_transform = carla.Transform(cone_car_location, carla.Rotation(pitch=0, yaw=-90, roll=0))
cone_car = world.spawn_actor(cone_car_bp, cone_car_transform)


cone_car_location1 = carla.Location(x=340.5, y=250, z=1.0)
cone_car_bp1 = blueprint_library.filter("vehicle.seat.leon")[0]
cone_car_transform1 = carla.Transform(cone_car_location1, carla.Rotation(pitch=0, yaw=-90, roll=0))
cone_car = world.spawn_actor(cone_car_bp1, cone_car_transform1)


