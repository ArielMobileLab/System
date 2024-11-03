

import carla
import random
import time
from nav_msgs.msg import Odometry
import rospy
import threading


# # # # find location of the traficlitts and then go ot the side that give me locatsion of map file~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# # # # Connect to the CARLA server
# # client = carla.Client('localhost', 2000)
# # client.set_timeout(10.0)

# # # # Load the world
# # world = client.get_world()

# # # # Retrieve all actors in the world
# # actors = world.get_actors()

# # # # Filter traffic lights from the actors
# # traffic_lights = actors.filter('traffic.traffic_light')

# # # # Function to find and print details of a traffic light by location or other criteria
# # def find_traffic_light_by_location(traffic_lights, target_location, tolerance=2.0):
# #     for traffic_light in traffic_lights:
# #         location = traffic_light.get_location()
# #         distance = location.distance(target_location)
# #         if distance < tolerance:
# #             print("Traffic Light ID: {}".format(traffic_light.id))
# #             print("Location: {}".format(location))
# #             print("Transform: {}".format(traffic_light.get_transform()))
# #             return traffic_light
# #     print("No traffic light found within the tolerance at the specified location.")
# #     return None

# # # Define the target location of the traffic light you are interested in
# # target_location = carla.Location(x=340, y=-1.2, z=0.499982)  # Example coordinates

# # # Find and print details of the traffic light at the target location
# # traffic_light = find_traffic_light_by_location(traffic_lights, target_location)

# # # You can also print all traffic light IDs and locations to identify the specific one you need
# # for traffic_light in traffic_lights:
# #     location = traffic_light.get_location()
# #     print("Traffic Light ID: {}, Location: {}".format(traffic_light.id, location))


# #chagen speseifc trafic light~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``

# import carla

# # Connect to the CARLA server
# client = carla.Client('localhost', 2000)
# client.set_timeout(10.0)

# # Load the world
# world = client.get_world()

# # Retrieve all actors in the world
# actors = world.get_actors()
# print("hiiiiiiiiiiiiiiiiiiiiiii")
# # Find the traffic light with ID 
# traffic_light_id = 63
# traffic_light = None
# ramzor = True



# def ramzor(data):
#     global ramzor



#     for actor in actors:
#             if actor.type_id.startswith("traffic.traffic_light") and actor.id == traffic_light_id:
#                 traffic_light = actor
#                 break

#         # Change the traffic light state if the specific traffic light is found
#     if traffic_light is not None:
#             traffic_light.set_state(carla.TrafficLightState.Red)
#             traffic_light.set_green_time(3)  # Optional: Set the green time duration
#             print("trafic changed")
#     else:
#             print("not found.")

#     ramzor = False



# if __name__ == '__main__':
          
     
#         rospy.init_node('message_listenerr')
#         # Subscribe to the topic that publishes the messages
#         rospy.Subscriber('/carla/ego_vehicle/odometry',Odometry, ramzor, queue_size=1)  

#         # Set the desired loop frequency (1 Hz)
#         rate = rospy.Rate(1)

#         # Continue running the code
#         while not rospy.is_shutdown():

#             # Sleep to maintain the desired loop frequency
#               rate.sleep()



import rospy
from nav_msgs.msg import Odometry
import threading

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load the world
world = client.get_world()

# Retrieve all actors in the world
actors = world.get_actors()

# Find the traffic light with ID 48
traffic_light_id = 63
traffic_light = None
ramzor_flag = True

for actor in actors:
    if actor.type_id.startswith("traffic.traffic_light") and actor.id == traffic_light_id:
        traffic_light = actor
        break

if traffic_light is None:
    rospy.logerr("Traffic light with ID 48 not found")
else:
    rospy.loginfo("Traffic light with ID 48 found")

# Function to set the traffic light state
def set_traffic_light_state(state, duration=None):
    if traffic_light is not None:
        traffic_light.set_state(state)
        if duration:
            traffic_light.set_green_time(duration)

# Callback function for the odometry subscriber
def ramzor(data):
    global ramzor_flag
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y

    if  ramzor_flag == True and 86 < x < 95 and  -267.0 < y < -250.0 :
        rospy.loginfo("Car is within the specified range")
        # Set traffic light to red
        traffic_light.set_state(carla.TrafficLightState.Red)
        rospy.loginfo("Traffic light set to red")

        # Set traffic light back to green after 4 seconds
        threading.Timer(10, lambda: traffic_light.set_state(carla.TrafficLightState.Green)).start()
        rospy.loginfo("Traffic light will be set to green in 10 seconds")
        ramzor_flag = False    

 
if __name__ == '__main__':
    rospy.init_node('traffic_light_control')
    rospy.loginfo("ROS node initialized")
    
    # Subscribe to the topic that publishes the messages
    rospy.Subscriber('/carla/ego_vehicle/odometry', Odometry, ramzor, queue_size=1)  

    rospy.loginfo("Subscribed to /carla/ego_vehicle/odometry")

    # Spin to keep the script running
    rospy.spin()
