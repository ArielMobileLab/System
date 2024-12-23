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

def Generate_Car1():
    # Create a blueprint for the vehicle
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = random.choice(blueprint_library.filter('vehicle.mini.cooper_s_2021'))

    # Define the spawn location for the vehicle
    spawn_location = carla.Transform(
        carla.Location(x=338.5, y=317.5, z=1.0),  # Initial location
        carla.Rotation(pitch=0, yaw=-90, roll=0)  # 180-degree rotation
    )
    # Spawn the vehicle
    vehicle = world.spawn_actor(vehicle_bp, spawn_location)
    vehicle.apply_control(carla.VehicleControl(throttle=0.55, steer=0.0))

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

    #if first_car_cross == True and 90 < data.pose.pose.position.x < 100 and -35 < data.pose.pose.position.y < -20:
    if first_car_cross == True and 275<data.pose.pose.position.x<293 and -139<data.pose.pose.position.y<-123:
        print("car_1")
        Generate_Car1()
        first_car_cross = False

# Main function
if __name__ == '__main__':
    rospy.init_node('message_listener646')

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
