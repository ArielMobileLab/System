import carla
import random
import time
from nav_msgs.msg import Odometry
import rospy


# List to store the created actors
created_actors = []

client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

# Load the CARLA world
world = client.get_world()
first_car_cross = True
second_car_cross = True
actors = world.get_actors()
print("car1~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# Iterate through all actors and find traffic lights
for actor in actors:
    if actor.type_id.startswith("traffic.traffic_light"):
        traffic_light = actor
        # Change the traffic light state to green (Assuming the state is "Green")
        traffic_light.set_state(carla.TrafficLightState.Green)
        traffic_light.set_green_time(10000)  # Optional: Set the green time duration

def Generate_Car1():
    # Create a blueprint for the vehicle
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = random.choice(blueprint_library.filter('vehicle.tesla.model3'))

    # Define the spawn location for the vehicle
    spawn_location = carla.Transform(
        carla.Location(x=117, y=2.43, z=0.5),  # Initial location
        carla.Rotation(pitch=0, yaw=0, roll=0)  # 180-degree rotation
    )
    # Spawn the vehicle
    vehicle = world.spawn_actor(vehicle_bp, spawn_location)
    vehicle.apply_control(carla.VehicleControl(throttle=0.5, steer=0.0))

    # Add the created actor to the list
    created_actors.append(vehicle)

    time.sleep(10)

    # Apply the brake light state to the vehicle
    brake_light_state = carla.VehicleLightState(carla.VehicleLightState.Brake)
    vehicle.set_light_state(carla.VehicleLightState(brake_light_state))
    vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0, brake=1.0))

    # Wait for 2 seconds
    time.sleep(2)

    # Resume driving slowly
    vehicle.apply_control(carla.VehicleControl(throttle=0.2, steer=0.0))


def cleanup():
    # Destroy all created actors
    for actor in created_actors:
        actor.destroy()

# Callback function for the subscriber
def Cars(data):
    world.tick()

    global first_car_cross
    global second_car_cross

    if first_car_cross == True and 90 < data.pose.pose.position.x < 100 and -35 < data.pose.pose.position.y < -20:
        print("car_1")
        Generate_Car1()
        first_car_cross = False

# Main function
if __name__ == '__main__':
    rospy.init_node('message_listener64')

    # Subscribe to the topic that publishes the messages
    rospy.Subscriber('/carla/ego_vehicle/odometry', Odometry, Cars, queue_size=1)

    # Set the desired loop frequency (1 Hz)
    rate = rospy.Rate(1)

    try:
        # Continue running the code
        while not rospy.is_shutdown():
            # Sleep to maintain the desired loop frequency
            rate.sleep()
    finally:
        # Cleanup and destroy actors when the script is interrupted
        cleanup()