from nav_msgs.msg import Odometry
import rospy
import threading
import carla
import math
from collections import OrderedDict
from datetime import datetime
import json
import os
import sys

# Connect to the CARLA server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load the world
world = client.get_world()

# Retrieve all actors in the world
actors = world.get_actors()

# Find the traffic light with the specified ID
traffic_light_id = 60
traffic_light = None
traffic_light_green_flag = 0
yellow_time = 3
acceleraion = 2



Map_type = sys.argv[1]
#Map_type = "Guide_parent"
#Map_type = "First_Response_train_2"
#Map_type = "First_Response"

Agent_type = "_Event"
folder_path = "/home/omer/Desktop/Carla_Logs/Logs"
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
file_name = os.path.join(folder_path, 'Traffic_Light{}_{}.json'.format(Agent_type, current_time))



def write_to_json(data_dict):
   
    # Open the JSON file in append mode and write the data
    with open(file_name, 'a') as json_file:
        json.dump(data_dict, json_file)
        json_file.write('\n')  # Add a newline for readability



# Locate the specified traffic light
for actor in actors:
    if actor.type_id.startswith("traffic.traffic_light") and actor.id == traffic_light_id:
        traffic_light = actor
        break

if traffic_light is None:
    rospy.logerr("Traffic light with ID {} not found".format(traffic_light_id))
else:
    rospy.loginfo("Traffic light with ID {} found".format(traffic_light_id))

    # Retrieve the traffic light's location
    traffic_light_transform = traffic_light.get_transform()
    traffic_light_location = traffic_light_transform.location
    traffic_light_x =  traffic_light_location.x
    traffic_light_y =  traffic_light_location.y


# Function to set the traffic light state
def set_traffic_light_state(state, duration=None):
    if traffic_light is not None:
        traffic_light.set_state(state)
        if duration and state == carla.TrafficLightState.Red:
            threading.Timer(duration, lambda: traffic_light.set_state(carla.TrafficLightState.Green)).start()
            rospy.loginfo("Traffic light will be set to green after {} seconds".format(duration))

def maximal_distance_for_must_cross_function(v,yellow_time):
    # Calculate the distance based on speed and defined parameters
    # the Junction_Width is deffrennt based on the junction and map
    Junction_Width = 7.5
    Vehicle_Length = 3.633375
    delay = 0.04
    distance = (v * (yellow_time+delay) - Junction_Width - Vehicle_Length)  
    return distance


def maximal_distance_for_must_stop_function(speed,yellow_time):
    acceleraion = 2
    delay = 0.04
    distance = (speed*(yellow_time+delay) - 0.5*acceleraion*yellow_time**2)  
    return distance



# Callback function for the odometry subscriber
def traffic_light_event(data):


    global traffic_light_green_flag
    ego_x = data.pose.pose.position.x
    ego_y = data.pose.pose.position.y

    if traffic_light_green_flag == 0 and 130<data.pose.pose.position.x<160 and -333<data.pose.pose.position.y<-323 :
        traffic_light_green_flag = 1 
          
    #traffic_light_green_flag  :


    if traffic_light_green_flag == 1:
          speed = math.sqrt(data.twist.twist.linear.x**2 + data.twist.twist.linear.y**2)
          #print(speed)
          # Get the ego vehicle's position
          

          # Calculate the distance from the ego vehicle to the traffic light
          distance_to_traffic_light = math.sqrt((traffic_light_x - ego_x)**2 + (traffic_light_y + ego_y)**2)
          #print("distance_to_traffic_light")
          #print(distance_to_traffic_light)

          maximal_distance_for_must_stop = maximal_distance_for_must_stop_function(speed,yellow_time)
          #print("maximal_distance_for_must_stop")
          #print(maximal_distance_for_must_stop)
          
          
          if maximal_distance_for_must_stop >= distance_to_traffic_light: 
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                # Simulation Time
                header = data.header
                secs = header.stamp.secs
                nsecs = header.stamp.nsecs
                simulation_Time = secs + nsecs * 1e-9
                simulation_Time_Ros = data.header.seq*0.033333335071821
                
                Egocar_data = OrderedDict()
                Egocar_data["Type"] = "Traffic_Light:"
                Egocar_data["World_Time"] = timestamp
                Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
                Egocar_data["Simulation_time"] = simulation_Time
                Egocar_data["Traffic_Light_Event"] = "Traffic_Light_Stop_A"
                write_to_json(Egocar_data) # for json


           
                # Set traffic light to yellow
                traffic_light.set_state(carla.TrafficLightState.Yellow)
                rospy.loginfo("Traffic light set to yellow")

                # Set traffic light to red after 3 seconds
                threading.Timer(yellow_time, lambda: set_traffic_light_state(carla.TrafficLightState.Red, duration=10)).start()
                traffic_light_green_flag = 0  # Disable further changes until reset

            

if __name__ == '__main__':
    rospy.init_node('traffic_light_controll')
    
    # Subscribe to the topic that publishes the messages
    rospy.Subscriber('/carla/ego_vehicle/odometry', Odometry, traffic_light_event, queue_size=1)  


    # Spin to keep the script running
    rospy.spin()
