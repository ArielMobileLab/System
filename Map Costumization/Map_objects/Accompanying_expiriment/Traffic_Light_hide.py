import carla
import time
import signal
import sys

def spawn_barrier(world, blueprint_library, location):
    blueprint = blueprint_library.find('static.prop.vendingmachine')
    transform = carla.Transform(location)
    barrier = world.spawn_actor(blueprint, transform)
    return barrier

def cleanup(barrier):
    if barrier is not None:
        print("Destroying barrier...")
        barrier.destroy()

def signal_handler(sig, frame):
    print("Signal received, cleaning up...")
    cleanup(barrier)
    sys.exit(0)

# Set up signal handling for clean termination
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    barrier_location = carla.Location(x=74.8, y=333, z=1)  # Adjust coordinates as needed

# Set the rotation for the barrier (rotate 90 degrees around the z-axis)
    barrier_rotation = carla.Rotation(pitch=90, yaw=180, roll=90)  # Adjust yaw as needed for 90 degrees rotation

# Create a transform with the location and rotation
    barrier_transform = carla.Transform(location=barrier_location, rotation=barrier_rotation)

    # Spawn the barrier
    barrier = spawn_barrier(world, blueprint_library, barrier_location)
    print("Barrier spawned at:", barrier_location)

    # Keep the script running to maintain the barrier
    while True:
        time.sleep(1)

except Exception as e:
    print("An error occurred:", e)
    cleanup(barrier)
finally:
    cleanup(barrier)

