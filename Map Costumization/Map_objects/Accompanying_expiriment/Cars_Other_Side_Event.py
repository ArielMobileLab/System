import carla
import random
import time
from nav_msgs.msg import Odometry
import rospy
import numpy as np


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
    vehicle_bp = random.choice(blueprint_library.filter('vehicle.tesla.model3'))

    # Define the spawn location for the vehicle
    spawn_location = carla.Transform(
        carla.Location(x=340, y=-1.2, z=0.499982),  # Initial location
        carla.Rotation(pitch=0, yaw=180, roll=0)  # 180-degree rotation
    )
    # Spawn the vehicle
    vehicle = world.spawn_actor(vehicle_bp, spawn_location)
    vehicle.apply_control(carla.VehicleControl(throttle=0.25, steer=0.0))

    # Add the created actor to the list
    created_actors.append(vehicle)

def Generate_Cars2(world, actors, num_cars=15):
    # Find the Nissan Micra actor
    for actor in actors:
        if actor.attributes.get('role_name') == 'ego_vehicle':
            ego_vehicle = actor
            break

    blueprint_library = world.get_blueprint_library()


    spawn_location = carla.Transform(
        carla.Location(x=110.0, y=330.5, z=0.499982)
    )


    created_actors = []

    min_gap = 10  # Minimum gap time
    max_gap = 18  # Maximum gap time

    # Spawn the vehicles
    for i in range(num_cars):
        nissan_micra_location = ego_vehicle.get_location()

        # Generate the spawn interval based on car position and the pre-generated gaps
        if nissan_micra_location.x > 240:
            # Use a uniform distribution to generate random intervals between min_gap and max_gap
            random_interval = np.random.uniform(min_gap, max_gap)
            
            print(random_interval)
            vehicle_bp = random.choice(blueprint_library.filter('vehicle.tesla.model3'))
            color_name = random.choice(['255,255,255', '128,128,128', '0,0,0','0,0,139'])
	    #black: '0,0,0'
	    #Grey: '128,128,128'
	    #White: '255,255,255'
	    #Dark Blue: '0,0,139'
            vehicle_bp.set_attribute('color', color_name)


            vehicle = world.spawn_actor(vehicle_bp, spawn_location)
            vehicle.apply_control(carla.VehicleControl(throttle=0.42, steer=0.0))  # throttle=0.42 original

            created_actors.append(vehicle)
            time.sleep(random_interval)  # Wait for the generated interval before spawning the next car


def cleanup():
    # Destroy all created actors
    for actor in created_actors:
        actor.destroy()

# Callback function for the subscriber
def Cars(data):
    world.tick()

    global first_car_cross
    global second_car_cross

    #if first_car_cross == True and 87.4309 < data.pose.pose.position.x < 93.3200: original
    if first_car_cross == True and 87.4309 < data.pose.pose.position.x < 93.3200:
        #print("first_Car")
        Generate_Car1()
        first_car_cross = False
    
    if second_car_cross == True  and  330.00 < data.pose.pose.position.x < 340.00 and -115.00 < data.pose.pose.position.y < -90.00:
    #if second_car_cross == True:
        #print("car_2")
        Generate_Cars2(world, actors, num_cars=15)
        second_car_cross = False

# Main function
if __name__ == '__main__':
    rospy.init_node('message_listener45')

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
