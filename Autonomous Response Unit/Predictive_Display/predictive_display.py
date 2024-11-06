import math
import time
import carla

# Connect to Carla
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
start_time = 0.0
# Get the world
world = client.get_world()

settings = world.get_settings()
settings.fixed_delta_seconds = 0.04
world.apply_settings(settings)

latency = 0.05
prediction_steps = 5

def on_world_tick(world_snapshot):
      # Start timing immediately upon entering the function
    
    ego_vehicle = None
    
    # Find the ego vehicle in the snapshot
    for actor_snapshot in world_snapshot:
        actor = world.get_actor(actor_snapshot.id)
        if actor and actor.attributes.get('role_name') == 'ego_vehicle':
            ego_vehicle = actor
            break

    if ego_vehicle is not None:
        # Get velocity
        velocity = ego_vehicle.get_velocity()
        speed = math.sqrt(velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2)
        ego_vehicle_transform = ego_vehicle.get_transform()
        location = ego_vehicle_transform.location
        forward_vector = ego_vehicle_transform.get_forward_vector()


        start = carla.Location(
            x=location.x + speed * 0.04 * forward_vector.x,
            y=location.y + speed * 0.04 * forward_vector.y,
            z=location.z + speed * 0.04 * forward_vector.z
        )

        end = carla.Location(
            x=start.x + (speed * latency + 1.4) * forward_vector.x,
            y=start.y + (speed * latency + 1.4) * forward_vector.y,
            z=start.z + (speed * latency + 1.4) * forward_vector.z
        )

        # Calculate elapsed time
        #elapsed_time = time.time() - start_time
        #print(elapsed_time)
        
        # Draw the line in the simulation
        world.debug.draw_line(
            carla.Location(start.x, start.y, 0.4),
            carla.Location(end.x, end.y, 0.4),
            thickness=1,
            color=carla.Color(r=0, g=0, b=0),
            life_time=0.041
        )

def main():
    #start_time = time.time()
    world.on_tick(lambda snapshot: on_world_tick(snapshot))
    
    while True:
        world.tick()

if __name__ == "__main__":
    main()
