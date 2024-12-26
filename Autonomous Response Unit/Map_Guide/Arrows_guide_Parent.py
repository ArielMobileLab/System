

#!/usr/bin/env python
import rospy
import cv2
import os
import matplotlib.pyplot as plt
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
import math
import time
import numpy as np
import sys
from rosgraph_msgs.msg import Log
import matplotlib
import sys
from collections import OrderedDict
from datetime import datetime
import json
import pygame
from nav_msgs.msg import Odometry



Map_type = sys.argv[1]
Folder_Name = sys.argv[2]
#Map_type = "Guide_Train"
#Map_type = "Guide_Spatial"



folder_path = "/home/omer/Desktop/Carla_Logs/Logs/{}".format(Folder_Name)
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
file_name = os.path.join(folder_path, 'Photo_Interapt_Status{}_{}.json'.format(Map_type,current_time))

RIGHT='/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/RIGHT.jpeg'
RIGHT_2='/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/RIGHT_2.jpeg'
LEFT='/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/LEFT.jpeg'
LEFT_2='/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/LEFT_2.jpeg'
#Brake='/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/brake.jpeg'
black_window='/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/A_black_image.jpeg'
#ACCIDENT = '/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/ACCIDENT.jpeg'
#Take_Control = '/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/Take_Control.jpeg'
#Right_100M = '/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/Right_100M.jpeg'
#Right_50M = '/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/Right_50M.jpeg'
#Right_Now = '/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/Right_Now.jpeg'
Front = '/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/Front.jpeg'


sec = 1

first_arrow = True
Secound_arrow = True
third_arrow = True
fourth_arrow = True
fifth_arrow = True
seven_errow = True
Brake_arrow = True
ten_arrow = True
eight_arrow = True
arrow_term = 0.0
Brake_blackWindow = True

plt.rcParams['toolbar'] = 'None'



def write_to_json(data_dict):
   
    # Open the JSON file in append mode and write the data
    with open(file_name, 'a') as json_file:
        json.dump(data_dict, json_file)
        json_file.write('\n')  # Add a newline for readability

def ShowArrow(photo_path, term):
    
    global arrow_term
    # create a figure and subplot
    fig, ax = plt.subplots(figsize=(2.5, 2.5))
    # remove margins
    fig.subplots_adjust(0, 0, 1, 1)
    # turn axes off
    ax.axis("off")

    # Try reading the image
    image = cv2.imread(photo_path)

    if image is not None:
        # Check the number of channels
        num_channels = image.shape[-1]

        if num_channels == 3 or num_channels == 4:
            manager = plt.get_current_fig_manager()
            manager.window.wm_geometry("+3580+10")

            # Calculate position to center the image at the top
            image_height, image_width, _ = image.shape
            display_width = 1  # Set to 1 to cover the entire width
            display_height = display_width * (image_height / image_width)

            # Calculate position to center the image at the top
            top_margin = 1 - display_height

            ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), extent=[0, display_width, top_margin, 1], aspect='auto')
            # remove frame
            fig.canvas.manager.window.overrideredirect(1)
            # Show the plot
            plt.ion()
            plt.show(block=False)  # block=False allows the script to continue without waiting for the window to be closed
            plt.pause(0.1)
            
            if term == 1 :
                while not (95.0 < arrow_term < 96.0):
                    pass
                plt.close(fig)
            if term == 2 : 
                while not (95.0 < arrow_term < 101.0):
                    pass
                plt.close(fig)
            if term == 3 : 
                while not (332.0 < arrow_term < 335.0):
                    pass
                plt.close(fig)  
            if term == 4 : 
                while not (327.0 < arrow_term < 330.0):
                    pass
                plt.close(fig) 
            if term == 5 : 
                time.sleep(10)
                plt.close(fig)  
            if term == 6 : 
                while not (3.0 < arrow_term < 4.8):
                    pass
                plt.close(fig)  

        else:
            print("Image has an unsupported number of channels.")
    else:
        print("Failed to read the image.")
    	   
def ShowArrow_C(photo_path, term):
    
    global arrow_term
    # create a figure and subplot
    fig, ax = plt.subplots(figsize=(2.5, 2.5))
    # remove margins
    fig.subplots_adjust(0, 0, 1, 1)
    # turn axes off
    ax.axis("off")

    # Try reading the image
    image = cv2.imread(photo_path)

    if image is not None:
        # Check the number of channels
        num_channels = image.shape[-1]

        if num_channels == 3 or num_channels == 4:
            manager = plt.get_current_fig_manager()
            manager.window.wm_geometry("+3580+10")

            # Calculate position to center the image at the top
            image_height, image_width, _ = image.shape
            display_width = 1  # Set to 1 to cover the entire width
            display_height = display_width * (image_height / image_width)

            # Calculate position to center the image at the top
            top_margin = 1 - display_height

            ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), extent=[0, display_width, top_margin, 1], aspect='auto')
            # remove frame
            fig.canvas.manager.window.overrideredirect(1)
            # Show the plot
            plt.ion()
            plt.show(block=False)  # block=False allows the script to continue without waiting for the window to be closed
            plt.pause(0.1)
            
            if term == 1 :
                while not (95.0 < arrow_term < 96.0):
                    pass
                plt.close(fig)
            if term == 2 : 
                while not (75 < arrow_term < 80):
                    pass
                plt.close(fig)

            if term == 3 :
                while not (85 < arrow_term < 90):
                    pass
                plt.close(fig)    

            if term == 4 :
                while not (101 < arrow_term < 105):
                    pass
                plt.close(fig)    

            if term == 5 :
                while not (329 < arrow_term < 354):
                    pass
                plt.close(fig)    

            if term == 6 : 
                while not (327.0 < arrow_term < 330.0):
                    pass
                plt.close(fig)   
            if term == 7 : 
                time.sleep(8)
                plt.close(fig)   

        
        
        else:
            print("Image has an unsupported number of channels.")
    else:
        print("Failed to read the image.")

def BrakeGas(photo_path, sec):
    # create a figure and subplot
    fig, ax = plt.subplots(figsize=(5, 5))
    # remove margins
    fig.subplots_adjust(0, 0, 1, 1)
    # turn axes off
    ax.axis("off")

    # Try reading the image
    image = cv2.imread(photo_path)

    if image is not None:
        # Check the number of channels
        num_channels = image.shape[-1]

        if num_channels == 3 or num_channels == 4:
            manager = plt.get_current_fig_manager()
            manager.window.wm_geometry("+2700+54")

            # Calculate position to center the image at the top
            image_height, image_width, _ = image.shape
            display_width = 1  # Set to 1 to cover the entire width
            display_height = display_width * (image_height / image_width)

            # Calculate position to center the image at the top
            top_margin = 1 - display_height

            ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), extent=[0, display_width, top_margin, 1], aspect='auto')
            # remove frame
            fig.canvas.manager.window.overrideredirect(1)
            # Show the plot
            plt.show(block=False)  # block=False allows the script to continue without waiting for the window to be closed
            plt.pause(sec)
            plt.close(fig)
        else:
            print("Image has an unsupported number of channels.")
    else:
        print("Failed to read the image.")

def blackWindow(photo_path, sec):

    # create a figure and subplot
    fig, ax = plt.subplots(figsize=(58, 50))
    # remove margins
    fig.subplots_adjust(0, 0, 1, 1)
    # turn axes off
    ax.axis("off")

    # Try reading the image
    image = cv2.imread(photo_path)

    if image is not None:
        # Check the number of channels
        num_channels = image.shape[-1]

        if num_channels == 3 or num_channels == 4:
            manager = plt.get_current_fig_manager()
            manager.window.wm_geometry("+0+0")

            # Calculate position to center the image at the top
            image_height, image_width, _ = image.shape
            display_width = 1  # Set to 1 to cover the entire width
            display_height = display_width * (image_height / image_width)

            # Calculate position to center the image at the top
            top_margin = 1 - display_height

            ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), extent=[0, display_width, top_margin, 1], aspect='auto')
            # remove frame
            fig.canvas.manager.window.overrideredirect(1)
            # Show the plot
            plt.show(block=False)  # block=False allows the script to continue without waiting for the window to be closed
            plt.pause(sec)
            plt.close(fig)
        else:
            print("Image has an unsupported number of channels.")
    else:
        print("Failed to read the image.")

def blackWindow(photo_path, sec):

    # create a figure and subplot
    fig, ax = plt.subplots(figsize=(58, 50))
    # remove margins
    fig.subplots_adjust(0, 0, 1, 1)
    # turn axes off
    ax.axis("off")

    # Try reading the image
    image = cv2.imread(photo_path)

    if image is not None:
        # Check the number of channels
        num_channels = image.shape[-1]

        if num_channels == 3 or num_channels == 4:
            manager = plt.get_current_fig_manager()
            manager.window.wm_geometry("+0+0")

            # Calculate position to center the image at the top
            image_height, image_width, _ = image.shape
            display_width = 1  # Set to 1 to cover the entire width
            display_height = display_width * (image_height / image_width)

            # Calculate position to center the image at the top
            top_margin = 1 - display_height

            ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), extent=[0, display_width, top_margin, 1], aspect='auto')
            # remove frame
            fig.canvas.manager.window.overrideredirect(1)
            # Show the plot
            plt.show(block=False)  # block=False allows the script to continue without waiting for the window to be closed
            plt.pause(sec)
            plt.close(fig)
        else:
            print("Image has an unsupported number of channels.")
    else:
        print("Failed to read the image.")
        
def Arrows(data):
    global first_arrow
    global Secound_arrow
    global third_arrow
    global fourth_arrow
    global fifth_arrow
    global eight_arrow
    global ten_arrow
    global Brake_arrow
    global arrow_term
    global Brake_blackWindow
    global seven_errow


    # World Time
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Simulation Time
    header = data.header
    secs = header.stamp.secs
    nsecs = header.stamp.nsecs
    simulation_Time = secs + nsecs * 1e-9
    simulation_Time_Ros = data.header.seq*0.033333335071821


    if Map_type == 'Guide_Train':

        if first_arrow == True and -9.37<data.pose.pose.position.x<0.96  and -252<data.pose.pose.position.y<-245:
            ShowArrow_Train(Front,7)

        if first_arrow == True and 187<data.pose.pose.position.x<195  and -143.3<data.pose.pose.position.y<-135:
            ShowArrow_Train(Front,6)

        if first_arrow == True and 187<data.pose.pose.position.x<195  and -212<data.pose.pose.position.y<-203:
            ShowArrow_Train(Front,6)

        if first_arrow == True and 115<data.pose.pose.position.x<124  and -308<data.pose.pose.position.y<-300:
            ShowArrow_Train(Front,7)

        if simulation_Time > 500 :
            blackWindow(black_window,20)


         

    if Map_type == 'Guide_Parent':
  


        if first_arrow == True and 141.5689<data.pose.pose.position.x<158.4301 and -61<data.pose.pose.position.y<-51: 

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "first_arrow"
            write_to_json(Egocar_data) # for json

            ShowArrow(RIGHT,1)
            first_arrow = False

        if Secound_arrow == True and 87.4309 < data.pose.pose.position.x < 93.3200 and -30<data.pose.pose.position.y<-15 :

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "Secound_arrow"
            write_to_json(Egocar_data) # for json

            ShowArrow(RIGHT,2)
            Secound_arrow = False

        if third_arrow == True and 250.5562<data.pose.pose.position.x<282.5260 and -3.0682<data.pose.pose.position.y<2.4960 :

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "third_arrow"
            write_to_json(Egocar_data) # for json

            ShowArrow(RIGHT_2,3)
            third_arrow = False   



        if fourth_arrow == True and 334.4758<data.pose.pose.position.x<339.3086 and -230.6557<data.pose.pose.position.y< -220.9451 :

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "fourth_arrow"
            write_to_json(Egocar_data) # for json


            ShowArrow(RIGHT,4)
            fourth_arrow = False    
            
            
        if fifth_arrow == True and 130<data.pose.pose.position.x<160 and -333<data.pose.pose.position.y<-323 :

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "fifth_arrow"
            write_to_json(Egocar_data) # for json

            ShowArrow(RIGHT_2,5)
            fifth_arrow = False    

        if -116.1248 < data.pose.pose.position.y < -90.128 and 88.2840 < data.pose.pose.position.x < 92.3620:

            if Brake_blackWindow == True:
                blackWindow(black_window,24)
                Brake_blackWindow = False


    if Map_type == 'Guide_Parent_C':

        if first_arrow == True and 141.5689<data.pose.pose.position.x<158.4301 and -61<data.pose.pose.position.y<-51: 
            print("1")
            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "first_arrow"
            write_to_json(Egocar_data) # for json

            ShowArrow_C(RIGHT,1)
            first_arrow = False

        if Secound_arrow == True and 87.4309 < data.pose.pose.position.x < 93.3200 and -30<data.pose.pose.position.y<-15 :
            print("2")
            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "Secound_arrow"
            write_to_json(Egocar_data) # for json

            ShowArrow_C(LEFT,2)
            Secound_arrow = False

        if third_arrow == True and 17<data.pose.pose.position.x<31 and -335<data.pose.pose.position.y<-320 :

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "third_arrow"
            write_to_json(Egocar_data) # for json

            ShowArrow_C(LEFT_2,3)
            third_arrow = False    

        if fourth_arrow == True and 82<data.pose.pose.position.x<98 and -186<data.pose.pose.position.y<-169 :

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "fourth_arrow"
            write_to_json(Egocar_data) # for json

            ShowArrow_C(RIGHT_2,4)
            fourth_arrow = False   

        if fifth_arrow == True and 275<data.pose.pose.position.x<293 and -139<data.pose.pose.position.y<-123 :

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "fifth_arrow"
            write_to_json(Egocar_data) # for json

            ShowArrow_C(RIGHT,5)
            fifth_arrow = False      
     

        if seven_errow == True and 334.4758<data.pose.pose.position.x<339.3086 and -230.6557<data.pose.pose.position.y< -220.9451 :

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "sixet_arrow"
            write_to_json(Egocar_data) # for json


            ShowArrow_C(RIGHT,6)
            seven_errow = False    

        if eight_arrow == True and 130<data.pose.pose.position.x<160 and -333<data.pose.pose.position.y<-323 :

            Egocar_data = OrderedDict()
            Egocar_data["Type"] = "Video_Status:"
            Egocar_data["World_Time"] = timestamp
            Egocar_data["Simulation_time_ROS"] = simulation_Time_Ros
            Egocar_data["Simulation_time"] = simulation_Time
            Egocar_data["Video"] = "seven_errow"
            write_to_json(Egocar_data) # for json

            ShowArrow_C(RIGHT_2,7)
            eight_arrow = False  

        if -116.1248 < data.pose.pose.position.y < -90.128 and 88.2840 < data.pose.pose.position.x < 92.3620:

            if Brake_blackWindow == True:
                blackWindow(black_window,24)
                Brake_blackWindow = False

    
def Close_Image(data):
    global arrow_term
    arrow_term = data.pose.pose.position.x 
    
      
	
    

# Initialize ROS node
rospy.init_node('Arrow_Guide')
matplotlib.use("TkAgg")

rospy.Subscriber('Odomerty_topic',Odometry, Arrows, queue_size=1)  
rospy.Subscriber('/carla/ego_vehicle/odometry',Odometry, Close_Image, queue_size=1)

rate = rospy.Rate(1)


# Continue running the code
while not rospy.is_shutdown():


   # if sample_rates:
   #     avg_sample_rate = sum(sample_rates) / len(sample_rates)
   #     print("Average Sample Rate:", avg_sample_rate, "Hz")
   # Sleep to maintain the desired loop frequency


   rate.sleep()
