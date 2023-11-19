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
        carla.Location(x=300, y=-2.0, z=0.499982),  # Initial location
        carla.Rotation(pitch=0, yaw=180, roll=0)  # 180-degree rotation
    )
    # Spawn the vehicle
    vehicle = world.spawn_actor(vehicle_bp, spawn_location)
    vehicle.apply_control(carla.VehicleControl(throttle=0.3, steer=0.0))

    # Add the created actor to the list
    created_actors.append(vehicle)

def Generate_Cars2():
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = random.choice(blueprint_library.filter('vehicle.tesla.model3'))

    # Define the spawn location for the vehicle
    spawn_location = carla.Transform(
        carla.Location(x=120.0, y=133.5, z=0.499982)
    )

    # Spawn the vehicle
    vehicle = world.spawn_actor(vehicle_bp, spawn_location)
    vehicle.apply_control(carla.VehicleControl(throttle=0.3, steer=0.0))

    # Add the created actor to the list
    created_actors.append(vehicle)

def cleanup():
    # Destroy all created actors
    for actor in created_actors:
        actor.destroy()

# Callback function for the subscriber
def Cars(data):
    world.tick()

    global first_car_cross
    global second_car_cross

    if first_car_cross == True and 92.3 < data.pose.pose.position.x < 92.4:
        print("car_1")
        Generate_Car1()
        first_car_cross = False

    if second_car_cross == True and 334.7 < data.pose.pose.position.x < 334.9:
        print("car_2")
        Generate_Cars2()
        second_car_cross = False

# Main function
if __name__ == '__main__':
    rospy.init_node('message_listener4')

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
