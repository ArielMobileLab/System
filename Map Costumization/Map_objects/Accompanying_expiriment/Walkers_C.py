import carla
import random
import logging
import glob
import os
import sys
import time
import weakref
import rospy
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry



# Add CARLA Python API to the system path
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


#Connect To carla Server as Client
client = carla.Client('localhost', 2000)
#Retrieve the CARLA world
world = client.get_world() 

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


# Lists to store vehicles, walkers, and actor IDs
walkers = []
all_id = []
all_actors = []

first_walker_cross_cond = True
secound_walker_cross_cond = True

def first_walker_cross():
    blueprint_library = world.get_blueprint_library()
    walker_bp = random.choice(blueprint_library.filter('walker.pedestrian.0002'))

    # Check if the walker blueprint has the 'is_invincible' attribute
    if walker_bp.has_attribute('is_invincible'):
        # Disable invincibility for the walker
        walker_bp.set_attribute('is_invincible', 'false')

    # Define the walker's initial location and transform
    spawn_point = carla.Transform(carla.Location(x=330.2, y=150, z=0.300000), carla.Rotation(yaw=0.0))

    # Spawn the walker actor
    walker = world.spawn_actor(walker_bp, spawn_point)

    # Create a controller for the walker
    walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
    walker_controller = world.spawn_actor(walker_controller_bp, carla.Transform(), walker)

    walker_controller.start()

    # Set the walker's target location
    target_location = carla.Location(x=330.2, y=200.86, z=0.300000)
    
    # Speed of the walker
    walker_controller.set_max_speed(1.2)
    
    walker_controller.go_to_location(target_location)
                 
def secound_walker_cross():
     
    blueprint_library = world.get_blueprint_library()
    walker_bp = random.choice(blueprint_library.filter('walker.pedestrian.0001'))

    # Check if the walker blueprint has the 'is_invincible' attribute
    if walker_bp.has_attribute('is_invincible'):
        # Disable invincibility for the walker
        walker_bp.set_attribute('is_invincible', 'false')


    # Define the walker's initial location and transform
    spawn_point = carla.Transform(carla.Location(x=346.90, y=5.85, z=0.300000), carla.Rotation(yaw=90.0))

    # Spawn the walker actor
    walker = world.spawn_actor(walker_bp, spawn_point)

    # Create a controller for the walker
    walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
    walker_controller = world.spawn_actor(walker_controller_bp, carla.Transform(), walker)

    walker_controller.start()
    # Set the walker's target location
    target_location = carla.Location(x=310.6, y=6.8, z=0.300000)
    #speed of the walker
    walker_controller.set_max_speed(1.2)
    
    walker_controller.go_to_location(target_location)

# Function to clean up and end the simulation
def cleanup(world, vehicles, client):
    all_actors = world.get_actors(all_id)
    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.no_rendering_mode = False
    settings.fixed_delta_seconds = None
    world.apply_settings(settings)

    # Stop walker controllers (list is [controller, actor, controller, actor ...])
    for i in range(0, len(all_id), 2):
        all_actors[i].stop()
        
    client.apply_batch([carla.command.DestroyActor(x) for x in all_id])


def Cross_Walker(data):
    global first_walker_cross_cond
    global secound_walker_cross_cond

    if first_walker_cross_cond == True and 200 <data.pose.pose.position.x<240 and -139<data.pose.pose.position.y< -124: 
    
       print("walker_1")
       first_walker_cross()
       first_walker_cross_cond = False

#    if secound_walker_cross_cond == True and 290.00<data.pose.pose.position.x<310.00 and -7.00<data.pose.pose.position.y<7.00 :
#        print("walker_2")
#        secound_walker_cross()
#        secound_walker_cross_cond = False
    
    
def cleanup(world, walkers, client):
    # Retrieve all actors with the specified IDs
    all_actors = world.get_actors(walkers)

    # Stop walker controllers (list is [controller, actor, controller, actor ...])
    for i in range(0, len(walkers), 2):
        all_actors[i].stop()

    # Destroy all actors
    client.apply_batch([carla.command.DestroyActor(x.id) for x in all_actors])

    # Reset the world settings
    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.fixed_delta_seconds = None
    world.apply_settings(settings) 



if __name__ == '__main__':
          
     
        rospy.init_node('message_listenerrRR')
        # Subscribe to the topic that publishes the messages
        rospy.Subscriber('/carla/ego_vehicle/odometry',Odometry, Cross_Walker, queue_size=1)  

        # Set the desired loop frequency (1 Hz)
        rate = rospy.Rate(1)

        try:

        # Continue running the code
            while not rospy.is_shutdown():

            # Sleep to maintain the desired loop frequency
              rate.sleep()

        finally:
            
            cleanup(world, walkers, client)
