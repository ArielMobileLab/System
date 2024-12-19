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


    # Create a WeatherParameters object
weather = carla.WeatherParameters(
cloudiness=0.0,
precipitation=0.0,
wind_intensity=0.0,
sun_altitude_angle=24.0,  # Adjust this angle for the sun's position
fog_density=0.0
)
    # Set the new weather parameters
world.set_weather(weather)


def Generate_Car1():
    # Create a blueprint for the vehicle
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = random.choice(blueprint_library.filter('vehicle.tesla.model3'))

    # Define the spawn location for the vehicle
    spawn_location = carla.Transform(
        #carla.Location(x=117, y=2.43, z=0.5),  # Initial location
        #carla.Rotation(pitch=0, yaw=0, roll=0)  # 180-degree rotation
        carla.Location(x=-2.5, y=10, z=0.300000),  # Initial location
        carla.Rotation(pitch=0, yaw=90.0, roll=0)  # 180-degree rotation
    )
    # Spawn the vehicle
    vehicle = world.spawn_actor(vehicle_bp, spawn_location)
    time.sleep(5)
    vehicle.apply_control(carla.VehicleControl(throttle=0.40 , steer=0.0))

    # Add the created actor to the list
    created_actors.append(vehicle)

    time.sleep(23)

    brake_light_state = carla.VehicleLightState(carla.VehicleLightState.Brake)

# Apply the brake light state to the vehicle
    vehicle.set_light_state(carla.VehicleLightState(brake_light_state)) 
    vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0,brake= 1.0))


    

def cleanup():
    # Destroy all created actors
    for actor in created_actors:
        actor.destroy()

# Callback function for the subscriber
def Cars(data):
    world.tick()

    global first_car_cross
    global second_car_cross

    if first_car_cross == True and 87.4309 < data.pose.pose.position.x < 93.3200 and -30 <data.pose.pose.position.y<- 15:
    #if first_car_cross == True :
 
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
