#!/usr/bin/env python

import rospy
import csv
import cv2
import os
import matplotlib.pyplot as plt
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
import math
import time
import numpy as np
import sys
from rosgraph_msgs.msg import Log
import matplotlib
import json
from carla_msgs.msg import CarlaStatus
from carla_msgs.msg import CarlaWorldInfo
from carla_msgs.msg import CarlaEgoVehicleStatus
from carla_msgs.msg import CarlaCollisionEvent
from collections import OrderedDict
from datetime import datetime
import time



simulation_time = 0.0
carla_world_time = 0.0
timestamp = 0.0
speed = 0.0
acceleration_x = 0.0
acceleration_y = 0.0
acceleration_z = 0.0
FileExist = False
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
folder_path = "/home/omer/Desktop/Carla_Logs"
file_name = os.path.join(folder_path, 'EgoCar_{}.json'.format(current_time))
#sys.path.append('/home/omer/Desktop/CARLA_0.9.13/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg')




	
#def Mental_Work_Load(data):
#    if data.data < 0.5:
        
#	    stop_data = OrderedDict()
#	    stop_data["Type"] = "Termination:"
#	    stop_data["Reson"] = "Aoutnumos stop"
#	    stop_data["Timestamp"] = timestamp
#	    stop_data["Simulation_time"] = simulation_time
    	    
#       write_to_json(stop_data)
#       rospy.signal_shutdown()

#     else :
#	pass


def my_shutdown_callback():
    
    # This function will be called when the ROS node is shutting down.
    rospy.loginfo("ROS node is shutting down. Performing cleanup...")
    
  
    stop_data = OrderedDict()
    stop_data["Type"] = "Termination:"
    stop_data["Reson"] = "Operator Stop"
    stop_data["Timestamp"] = timestamp
    stop_data["Simulation_time"] = simulation_time
   
    write_to_json(stop_data)


def collision_callback(data):
    
    intensity = math.sqrt(data.normal_impulse.x**2 +
                              data.normal_impulse.y**2 + data.normal_impulse.z**2)
    actor_id = data.other_actor_id
    
    
    collision_data = OrderedDict()
    collision_data["Type"] = "Termination:"
    collision_data["Reson"] = "Crash"
    collision_data["Timestamp"] = timestamp
    collision_data["Simulation_time"] = simulation_time
    collision_data["Actor_id"] = actor_id
    collision_data["Intensity"] = intensity

    write_to_json(collision_data)
    
    
    
#def Odemetry(data):
    

#    if 190.776831<data.pose.pose.position.x<191.722782898:
#        stop_data = OrderedDict()
#        stop_data["Type"] = "Termination:"
#        stop_data["Reson"] = "Finished"
#        stop_data["Timestamp"] = timestamp
#        stop_data["Simulation_time"] = simulation_time
        
#        write_to_json(stop_data) 

#        rospy.signal_shutdown('Finished')
#    else:
#        pass


def speed_callback(data):
  
   global speed
   velocity = data.velocity
   speed=round(velocity * 3.6, 1)
   

    

def gnss_callback(data):

    global simulation_time
    global timestamp

    latitude = data.latitude
    longitude = data.longitude
    timestamp = time.time() * 1000 

    simulation_time = data.header.seq*0.033333335071821 #matlab 
    


    # Create a dictionary for the current GNSS data
    Egocar_data = OrderedDict()
    Egocar_data["Type"] = "Ego car Sensors:"
    Egocar_data["Timestamp"] = timestamp
    Egocar_data["Simulation_time"] = simulation_time
    Egocar_data["Latitude"] = latitude
    Egocar_data["Longitude"] = longitude
    Egocar_data["Acceleration_x"] = acceleration_x
    Egocar_data["Acceleration_y"] = acceleration_y
    Egocar_data["Acceleration_z"] = acceleration_z
    Egocar_data["Speed"] = speed
    

    #write_to_csv(gnss_data) # for csv

    write_to_json(Egocar_data) # for json




def imu_callback(data):

    global acceleration_x
    global acceleration_y
    global acceleration_z


    acceleration_x = data.linear_acceleration.x
    acceleration_y = data.linear_acceleration.y
    acceleration_z = data.linear_acceleration.z
    


#write to json file
def write_to_json(data_dict):

   
    # Open the JSON file in append mode and write the data
    with open(file_name, 'a') as json_file:
        json.dump(data_dict, json_file)
        json_file.write('\n')  # Add a newline for readability

#write to csv file
#def write_to_csv(data):
#    csv_file = 'Object_data.csv'
#    # Open the CSV file in append mode and write the data
#    with open(csv_file, 'a', newline='') as csv_file:
#        csv_writer = csv.writer(csv_file)

#        # Write the data as a row in the CSV file
#        csv_writer.writerow(data.values())
    

def main():

    rospy.init_node('sensor_data_receiver')
    
    # Subscribe to the GNSS and IMU topics
    rospy.Subscriber("/carla/ego_vehicle/gnss", NavSatFix, gnss_callback)
    rospy.Subscriber("/carla/ego_vehicle/imu", Imu, imu_callback)
    rospy.Subscriber("/carla/ego_vehicle/vehicle_status", CarlaEgoVehicleStatus, speed_callback, queue_size=10)
    rospy.Subscriber("/carla/ego_vehicle/collision", CarlaCollisionEvent, collision_callback)
    rospy.Subscriber("/carla/ego_vehicle/odometry", Imu, imu_callback)
    #rospy.Subscriber('/carla/ego_vehicle/odometry',Odometry, Odemetry, queue_size=1) 
    #rospy.Subscriber("/HR", Float64, Mental_Work_Load)
    
 
    
    rospy.on_shutdown(my_shutdown_callback)
    
    rospy.spin()  # Keep the script running

if __name__ == '__main__':
    main()
