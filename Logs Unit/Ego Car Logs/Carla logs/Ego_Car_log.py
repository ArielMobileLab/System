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
from std_msgs.msg import Float32, Int8, Float64, Float32
from sensor_msgs.msg import Joy
from datetime import datetime
import carla
from carla_msgs.msg import CarlaEgoVehicleControl
import subprocess



client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()
world.wait_for_tick()

actor_id = None

    # Find the actor ID by type
actors = world.get_actors()
for actor in actors:
        if actor.attributes.get('role_name') == 'ego_vehicle':
            ego_vehicle = actor
            actor_id = actor.id
            break



Agent_type = sys.argv[1]
#Agent_type = 'test'

simulation_time = 0.0
carla_world_time = 0.0
timestamp = 0.0
speed = 0.0
acceleration_x = 0.0
acceleration_y = 0.0
acceleration_z = 0.0
velocity_x = 0.0
velocity_y = 0.0
velocity_z = 0.0
angular_velocity_roll = 0.0
angular_velocity_pitch = 0.0
angular_velocity_yaw = 0.0
FileExist = False
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
folder_path = "/home/omer/Desktop/Carla_Logs/Logs"
file_name = os.path.join(folder_path, 'EgoCar_{}_{}.json'.format(Agent_type, current_time))
#sys.path.append('/home/omer/Desktop/CARLA_0.9.13/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg')
FrameID = 0.0
orientation_x = 0.0
orientation_y = 0.0 
orientation_z = 0.0 
orientation_w = 0.0
gas = 0.0
brake = 0.0
sterring = 0.0 
write_to_json_flag = True  
log_closed = False
flag_my_shutdown_callback = True
potition_x = 0.0
potition_y = 0.0
gear = 0.0
potition_z = 0.0 
frame_id_counter = 0


	
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
  
        global write_to_json_flag
        global FrameID
	global flag_my_shutdown_callback
        

        # This function will be called when the ROS node is shutting down.
        rospy.loginfo("ROS node is shutting down. Performing cleanup...")
        
        
    
        stop_data = OrderedDict()
        stop_data["Type"] = "Termination"
        stop_data["WorldTime"] = timestamp
        stop_data["SimulationTime"] = simulation_time
        stop_data["FrameID"] = generate_frame_id()  
        stop_data["Reason"] = "Operator Stop"
        if flag_my_shutdown_callback == True:
		write_to_json(stop_data,add_comma=False)
		close_json_file()
		#close_json_file()
        
    
        write_to_json_flag = False

def collision_callback(data):
    global write_to_json_flag
    global collision_flag
    global log_closed  # Add the global variable
    global flag_my_shutdown_callback

    if write_to_json_flag and not log_closed:
        actor_id = data.other_actor_id

        client = carla.Client('127.0.0.1', 2000)
        world = client.get_world()  # Make sure to obtain the actual world instance
        actor = world.get_actor(actor_id)


        # Check if the actor is valid
        if actor:
            	actor_info =  actor
		actor_info = str(actor)
		start_index = actor_info.find("type=") + len("type=")
		end_index = actor_info.find(")", start_index)
		actor_name = actor_info[start_index:end_index].strip()
		

        else:
            	actor_name = "Unknown"

        stop_data = OrderedDict()
        stop_data["Type"] = "Termination"
        stop_data["WorldTime"] = timestamp
        stop_data["SimulationTime"] = simulation_time
        stop_data["FrameID"] = generate_frame_id()
        stop_data["Reason"] = "Crash" + "-" + actor_name

        write_to_json(stop_data, add_comma=False)
        log_closed = True  # Set the flag to True to indicate that the log is closed
        close_json_file()  # Call the close function here
        write_to_json_flag = False  # Set the flag to False after writing the last entry
	flag_my_shutdown_callback = False

   
#def Odemetry(data):
    

#    if 190.776831<data.pose.pose.position.x<191.722782898:
#        stop_data = OrderedDict()
#        stop_data["Type"] = "Termination"
#        stop_data["Reson"] = "Finished"
#        stop_data["Timestamp"] = timestamp
#        stop_data["Simulation_time"] = simulation_time
        
#        write_to_json(stop_data) 

#        rospy.signal_shutdown('Finished')
#    else:
#        pass


def speed_callback(data):
  
   global speed
   velocity = data.data
   speed = velocity*3.6
   
def generate_frame_id():
    global frame_id_counter
    frame_id_counter += 1
    return frame_id_counter
    

def gnss_callback(data):

    global simulation_time
    global timestamp
    global FrameID
    global potition_x
    global potition_y
    global potition_z


    latitude = data.latitude
    longitude = data.longitude
    altitude = data.altitude
    timestamp = datetime.now().strftime('%H:%M:%S.%f')
    #timestamp = time.time() * 1000 / 1000
    #dt_object = datetime.utcfromtimestamp(timestamp)
    #formatted_time = dt_object.strftime('%H:%M:%S.%f')[:-3]
    FrameID += 1
    

    simulation_time = data.header.seq*0.033333335071821 #matlab 
    
 
    # Create a dictionary for the current GNSS data
    Egocar_data = OrderedDict()
    Egocar_data["Type"] = "GPS"
    Egocar_data["WorldTime"] = timestamp
    Egocar_data["SimulationTime"] = simulation_time
    Egocar_data["FrameID"] = generate_frame_id() 
    Egocar_data["SimulationPosition"] = {"x": potition_x, "y": potition_y, "z": potition_z} 
    Egocar_data["Latitude"] = latitude
    Egocar_data["Longitude"] = longitude
    Egocar_data["Altitude"] = altitude
    Egocar_data["Orientation"] = {"x": orientation_x, "y": orientation_y, "z": orientation_z}
    Egocar_data["Speed"] = speed
    Egocar_data["Acceleration"] = {"x": acceleration_x, "y": acceleration_y, "z": acceleration_z}
    Egocar_data["VelocityLocal3D"] = {"x": velocity_x, "y": velocity_y, "z": velocity_z}
    Egocar_data["AngularAccelerationLocal3D"] = {"x": angular_velocity_roll, "y": angular_velocity_pitch, "z": angular_velocity_yaw}


    #write_to_csv(Egocar_data) # for csv
    write_to_json(Egocar_data,add_comma=True) # for json

    


def imu_callback(data):

    global acceleration_x
    global acceleration_y
    global acceleration_z


    acceleration_x = data.linear_acceleration.x
    acceleration_y = data.linear_acceleration.y
    acceleration_z = data.linear_acceleration.z

def odometry_callback(data):
    global actor_id
    global gear
    global orientation_x
    global orientation_y
    global orientation_z
    global velocity_x
    global velocity_y
    global velocity_z
    global angular_velocity_roll
    global angular_velocity_pitch
    global angular_velocity_yaw
    global write_to_json_flag
    global collision_flag
    global log_closed  # Add the global variable
    global flag_my_shutdown_callback
    global potition_x
    global potition_y
    global potition_z
    global Agent_type

    vehicle = client.get_world().get_actor(actor_id)
    gear = vehicle.get_control().gear

    potition_x = data.pose.pose.position.x
    potition_y = data.pose.pose.position.y
    potition_z = data.pose.pose.position.z
    orientation_x = data.pose.pose.orientation.x
    orientation_x = data.pose.pose.orientation.y  
    orientation_x = data.pose.pose.orientation.z 
    velocity_x = data.twist.twist.linear.x
    velocity_y = data.twist.twist.linear.y
    velocity_z = data.twist.twist.linear.z
    angular_velocity_roll = data.twist.twist.angular.x
    angular_velocity_pitch = data.twist.twist.angular.y
    angular_velocity_yaw = data.twist.twist.angular.z


    Egocar_data = OrderedDict()
    Egocar_data["Type"] = "CarTelemetries"
    Egocar_data["WorldTime"] = timestamp
    Egocar_data["SimulationTime"] = simulation_time
    Egocar_data["FrameID"] = generate_frame_id()
    Egocar_data["Speed"] = speed
    Egocar_data["Acceleration"] = acceleration_x
    Egocar_data["SteeringAngle"] = sterring
    Egocar_data["Brake"] = brake
    Egocar_data["Gas"] = gas
    Egocar_data["Gear"] = gear
    
    write_to_json(Egocar_data,add_comma=True)
    if Agent_type == "Face_Train":
	    if  data.header.seq*0.033333335071821 > 160:
			print("Log Finished by End of the simulation ")
			if write_to_json_flag and not log_closed:
			    stop_data = OrderedDict()
			    stop_data["Type"] = "Termination"
			    stop_data["WorldTime"] = timestamp
			    stop_data["SimulationTime"] = simulation_time
			    stop_data["FrameID"] = generate_frame_id()
			    stop_data["Reason"] = "End of the simulation"

			    if flag_my_shutdown_callback:
				write_to_json(stop_data, add_comma=False)
				#close_json_file()
				log_closed = True
				write_to_json_flag = False
    else:
	    if -116.1248 < data.pose.pose.position.y < -90.128 and 88.2840 < data.pose.pose.position.x < 92.3620:
		print("Log Finished by End of the simulation ")
		if write_to_json_flag and not log_closed:
		    stop_data = OrderedDict()
		    stop_data["Type"] = "Termination"
		    stop_data["WorldTime"] = timestamp
		    stop_data["SimulationTime"] = simulation_time
		    stop_data["FrameID"] = generate_frame_id()
		    stop_data["Reason"] = "End of the simulation"

		    if flag_my_shutdown_callback:
		        write_to_json(stop_data, add_comma=False)
		        #close_json_file()
		        log_closed = True
		        write_to_json_flag = False

            


def control_callback(data):

    global gas
    global brake
    global sterring

    sterring = data.steer
    brake = data.brake
    gas = data.throttle

   
def write_to_json(data_dict, add_comma=True):
    global write_to_json_flag
    if write_to_json_flag:
        with open(file_name, 'a') as json_file:
            json.dump(data_dict, json_file, indent=2)  # Add indentation for better readability
            if add_comma:
                json_file.write(',\n')  # Add a comma and newline for proper JSON formatting
            else:
                json_file.write('\n')  # Add newline without a comma


def close_json_file():
    with open(file_name, 'a') as json_file:
        json_file.write('\n]}\n')            

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

    with open(file_name, 'w') as json_file:
        json_file.write('{"Logs": [\n')

    # Subscribe to the GNSS and IMU topics
    rospy.Subscriber("/carla/ego_vehicle/gnss", NavSatFix, gnss_callback)
    rospy.Subscriber("/carla/ego_vehicle/imu", Imu, imu_callback)
    #rospy.Subscriber("/carla/ego_vehicle/vehicle_status", CarlaEgoVehicleStatus, speed_callback, queue_size=10)
    rospy.Subscriber("/carla/ego_vehicle/collision", CarlaCollisionEvent, collision_callback)
    rospy.Subscriber("/carla/ego_vehicle/odometry", Odometry, odometry_callback)
    rospy.Subscriber("/carla/ego_vehicle/speedometer", Float32, speed_callback, queue_size=10)
    #rospy.Subscriber("/HR", Float64, Mental_Work_Load)
    rospy.Subscriber("/carla/ego_vehicle/vehicle_control_cmd_manual", CarlaEgoVehicleControl, control_callback)
    
    

    
    rospy.on_shutdown(my_shutdown_callback)
    
    rospy.spin()  # Keep the script running

    

if __name__ == '__main__':
    main()
