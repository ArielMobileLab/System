import carla
import random
import time

def main():
    # Connect to the client and get the world
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    
    # Get the blueprint library and filter for walker blueprints
    blueprint_library = world.get_blueprint_library()
    walker_blueprints = blueprint_library.filter('walker.pedestrian.*')
    
    # Create a list to keep track of the spawned actors
    static_walkers = []
    
    # Set random seed for reproducibility
    random.seed(10)
    
    # Function to spawn a random walker at a given location
    def spawn_static_walker(location):
        walker_bp = random.choice(walker_blueprints)
        walker_transform = carla.Transform(location)
        walker = world.try_spawn_actor(walker_bp, walker_transform)
        if walker:
            static_walkers.append(walker)
    
    # Spawn 20 walkers at random locations
    for _ in range(30):
        spawn_point = world.get_random_location_from_navigation()
        if spawn_point:
            spawn_static_walker(spawn_point)
    
    print('Spawned 20 static walkers')
    
    try:
        # Keep the script running to maintain the walkers
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted by user. Destroying actors...')
    finally:
        for walker in static_walkers:
            walker.destroy()
        print('Actors destroyed')

if __name__ == '__main__':
    main()

