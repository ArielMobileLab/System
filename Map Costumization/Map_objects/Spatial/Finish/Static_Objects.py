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
cone_bp = blueprint_library.filter("static.prop.streetbarrier")[0] 
cone_location = carla.Location(x=245.699997, y=128, z=0.1)
cone_transform = carla.Transform(cone_location, carla.Rotation(pitch=0, yaw=90.0, roll=0))
cone = world.spawn_actor(cone_bp, cone_transform)

cone_bp1 = blueprint_library.filter("static.prop.streetbarrier")[0] 
cone_location1 = carla.Location(x=245.699997, y=130, z=0.1)
cone_transform1 = carla.Transform(cone_location1, carla.Rotation(pitch=0, yaw=90.0, roll=0))
cone1 = world.spawn_actor(cone_bp1, cone_transform1)

warning = blueprint_library.filter("static.prop.streetbarrier")[0] 
warning_location = carla.Location(x=245.699997, y=126, z=0.1)
warning_transform = carla.Transform(warning_location, carla.Rotation(pitch=0, yaw=90.0, roll=0))
warning = world.spawn_actor(warning, warning_transform)

car_location = carla.Location(x=198.0, y=2.020034, z=0.300000)
car_bp = blueprint_library.filter("vehicle.audi.tt")[0]
car_transform = carla.Transform(car_location, carla.Rotation(pitch=0, yaw=0, roll=0))
car = world.spawn_actor(car_bp, car_transform)

cone_car_location = carla.Location(x=242, y=129.750061, z=0.300000)
cone_car_bp = blueprint_library.filter("vehicle.dodge.charger_police")[0]
cone_car_transform = carla.Transform(cone_car_location, carla.Rotation(pitch=0, yaw=180, roll=0))
cone_car = world.spawn_actor(cone_car_bp, cone_car_transform)

#finally:
#    # Clean up actors and disconnect from CARLA
#    if 'cone' in locals():
#        cone.destroy()
#    if 'car' in locals():
#        car.destroy()
#    if 'cone_car' in locals():
#        cone_car.destroy()
#    if 'cone1' in locals():
#        cone1.destroy()
#    if 'warning' in locals():
#        warning.destroy()
   
#    print("Done!")

