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
   

    # Define traffic behavior in and around the work zone
    # You can control vehicle behavior using the CARLA Python API
    # For control the trafic lights~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    actors = world.get_actors()

            # Iterate through all actors and find traffic lights
    for actor in actors:
            if actor.type_id.startswith("traffic.traffic_light"):
                traffic_light = actor

            # Change the traffic light state to green (Assuming the state is "Green")
                traffic_light.set_state(carla.TrafficLightState.Green)
                traffic_light.set_green_time(10000)  # Optional: Set the green time duration


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


