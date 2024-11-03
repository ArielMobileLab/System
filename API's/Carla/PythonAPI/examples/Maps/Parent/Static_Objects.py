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
cone_bp1 = blueprint_library.filter("static.prop.streetbarrier")[0] 
cone_location1 = carla.Location(x=245.699997, y=327, z=0.1)
cone_transform1 = carla.Transform(cone_location1, carla.Rotation(pitch=0, yaw=90.0, roll=0))
cone1 = world.spawn_actor(cone_bp1, cone_transform1)

warning = blueprint_library.filter("static.prop.streetbarrier")[0] 
warning_location = carla.Location(x=245.699997, y=323, z=0.1)
warning_transform = carla.Transform(warning_location, carla.Rotation(pitch=0, yaw=90.0, roll=0))
warning = world.spawn_actor(warning, warning_transform)


cone_car_location = carla.Location(x=242, y=326.750061, z=0.300000)
cone_car_bp = blueprint_library.filter("vehicle.dodge.charger_police")[0]
cone_car_transform = carla.Transform(cone_car_location, carla.Rotation(pitch=0, yaw=180, roll=0))
cone_car = world.spawn_actor(cone_car_bp, cone_car_transform)

