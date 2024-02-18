#The code is responsible for
#    1) Changing the color of traffic lights
#    2) Launch of dynamic cars on the map

import carla
import random
import time
from nav_msgs.msg import Odometry
import rospy


# List to store the created actors for cleaning
created_actors = []

#connecot to the server
client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

first_car_cross = True
second_car_cross = True

# Load the CARLA world
world = client.get_world()
actors = world.get_actors()

# Iterate through all actors, find traffic lights to make them green 
for actor in actors:
    if actor.type_id.startswith("traffic.traffic_light"):
        traffic_light = actor
        # Change the traffic light state to green (Assuming the state is "Green")
        traffic_light.set_state(carla.TrafficLightState.Green)
        traffic_light.set_green_time(10000)  # Optional: Set the green time duration


def Generate_cars_first_vehicle_obstacle():
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


def Generate_cars_secound_vehicle_obstacle(world, actors, num_cars=15):

    # Find the Ego car actor
    for actor in actors:
        if actor.attributes.get('role_name') == 'ego_vehicle':
            ego_vehicle = actor
            break

    blueprint_library = world.get_blueprint_library()
    vehicle_bp = random.choice(blueprint_library.filter('vehicle.tesla.model3'))

    spawn_location = carla.Transform(
        carla.Location(x=110.0, y=133.5, z=0.499982)
    )

    amount_of_cars_driving_with_difficult_gap = 10

    created_actors = []

    # Spawn the vehicles
    for i in range(num_cars):

        #ego car location
        ego_car_location = ego_vehicle.get_location()
        ego_car_x-axis_location=ego_car.x

        #generate only before the optical, the x location of the ego car is parallel to the x location of the police car
        if ego_car_x-axis_location > 240:

            if i < amount_of_cars_driving_with_difficult_gap:
                #dificalt gap in sec
                gap_sec = 15.0
                
            else:
                #easy gap in sec
                gap_sec = 18.0

            vehicle = world.spawn_actor(vehicle_bp, spawn_location)
            vehicle.apply_control(carla.VehicleControl(throttle=0.35, steer=0.0))
            created_actors.append(vehicle)
            time.sleep(gap_sec)

def cleanup():
    # Destroy all created actors
    for actor in created_actors:
        actor.destroy()

# Callback function for the subscriber
def dynamic_car_generation(data):
    world.tick()

    global first_car_cross
    global second_car_cross

    if first_car_cross == True and 87.4309 < data.pose.pose.position.x < 93.3200:
        print("car_1")
        Generate_cars_first_vehicle_obstacle()
        first_car_cross = False
        
    if second_car_cross == True and 334.0 < data.pose.pose.position.x < 339.7652:
        print("car_2")
        #obstacle with gap acceptence
        Generate_cars_secound_vehicle_obstacle(world, actors, num_cars=15)
        second_car_cross = False

# Main function
if __name__ == '__main__':
    rospy.init_node('message_listener4')

    # Subscribe to the topic that publishes the messages
    rospy.Subscriber('Odomerty_topic', Odometry, dynamic_car_generation, queue_size=1)

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
