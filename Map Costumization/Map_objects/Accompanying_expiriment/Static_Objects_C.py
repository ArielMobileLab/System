import carla


# Connect to CARLA Server as a Client
client = carla.Client('localhost', 2000)
# Retrieve the CARLA world
world = client.get_world()

    # Create a WeatherParameters object
weather = carla.WeatherParameters(
cloudiness=0.0,
precipitation=0.0,
wind_intensity=0.0,
sun_altitude_angle=24.0,  # Adjust this angle for the sun's position
fog_density=0.0
)
    # Set the new weather parameters
world.set_weather(weather)


    # Generate cones and cars
    # Define work zone locations (You can adjust these coordinates)
    

    # Create a traffic cone
blueprint_library = world.get_blueprint_library()



cone_car_location = carla.Location(x=280, y=326.0, z=1.0)
cone_car_bp = blueprint_library.filter("vehicle.audi.tt")[0]
cone_car_transform = carla.Transform(cone_car_location, carla.Rotation(pitch=0, yaw=180, roll=0))
cone_car = world.spawn_actor(cone_car_bp, cone_car_transform)



warning1 = blueprint_library.filter("vehicle.ford.crown")[0]
warning1_location = carla.Location(x=235, y=128, z=0.5)
warning1_transform = carla.Transform(warning1_location, carla.Rotation(pitch=0, yaw=0, roll=0))
warning1 = world.spawn_actor(warning1, warning1_transform)



