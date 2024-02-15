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
    vehicle_bp = random.choice(blueprint_library.filter('vehicle.tesla.model3'))

    spawn_location = carla.Transform(
        carla.Location(x=110.0, y=133.5, z=0.499982)
    )

    num_cars_with_interval_15_sec = 10

    created_actors = []

    # Spawn the vehicles
    for i in range(num_cars):
        nissan_micra_location = ego_vehicle.get_location()

        #generate only before the apstical
        if nissan_micra_location.x > 240:

            if i < num_cars_with_interval_15_sec:

                current_interval = 15.0
                
            else:
                current_interval = 18.0

            vehicle = world.spawn_actor(vehicle_bp, spawn_location)
            vehicle.apply_control(carla.VehicleControl(throttle=0.35, steer=0.0))

            created_actors.append(vehicle)

            time.sleep(current_interval)

    

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
        print("car_1")
        Generate_Car1()
        first_car_cross = False
    #if first_car_cross == True and 334.0 < data.pose.pose.position.x < 339.7652: original
    if second_car_cross == True and 334.0 < data.pose.pose.position.x < 339.7652:
        print("car_2")
        Generate_Cars2(world, actors, num_cars=15)
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
