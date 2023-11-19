import carla

try:
    # Connect to CARLA Server as a Client
    client = carla.Client('localhost', 2000)
    # Retrieve the CARLA world
    world = client.get_world()
    # Set up the simulator in synchronous mode
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    # Generate cones and cars
    # Define work zone locations (You can adjust these coordinates)
    cone_location = carla.Location(x=237.699997, y=129.750000, z=0.300000)

    # Create a traffic cone
    blueprint_library = world.get_blueprint_library()
  

 
    cone_car_location = carla.Location(x=103, y=-188.483154, z=0.3)
    cone_car_bp = blueprint_library.filter("vehicle.carlamotors.carlacola")[0]
    cone_car_transform = carla.Transform(cone_car_location, carla.Rotation(pitch=0, yaw=180, roll=0))
    cone_car = world.spawn_actor(cone_car_bp, cone_car_transform)

    #103, -188.483154, 0.499982
    # Run the simulation
    while True:
        world.tick()

finally:
    # Clean up actors and disconnect from CARLA
    if 'cone' in locals():
        cone.destroy()
    if 'car' in locals():
        car.destroy()
    if 'cone_car' in locals():
        cone_car.destroy()
   
    print("Done!")

