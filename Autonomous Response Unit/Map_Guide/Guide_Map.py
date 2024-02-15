

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
#Map_type = "Guide_Train"
#Map_type = "Guide_Spatial"



RIGHT='/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/RIGHT.jpeg'
LEFT='/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/LEFT.jpeg'
Brake='/home/omer/Desktop/Autonomous Resope Unit/Arrow_Guide/brake.jpeg'

sec = 1

first_arrow = True
Secound_arrow = True
third_arrow = True
fourth_arrow = True
fifth_arrow = True
Brake_arrow = True
arrow_term = 0.0

plt.rcParams['toolbar'] = 'None'


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
                while not (89.0 < arrow_term < 95.0):
                    pass
                plt.close(fig)  
            if term == 6 : 
                while not (3.0 < arrow_term < 4.8):
                    pass
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





def Arrows(data):
    global first_arrow
    global Secound_arrow
    global third_arrow
    global fourth_arrow
    global fifth_arrow
    global Brake_arrow
    global arrow_term

    if Map_type == 'Guide_Train':

        if Brake_arrow == True:
            BrakeGas(Brake,6)
            print("hi 1 ")
            Brake_arrow = False

        if first_arrow == True and -8.5649<data.pose.pose.position.x<-1.6586  and -183.0030<data.pose.pose.position.y<-169.0352:
            ShowArrow(RIGHT,6)
           
	    

    if Map_type == 'Guide_Spatial':
        
        if Brake_arrow == True:
            BrakeGas(Brake,5)
            print("hi 2 ")
            Brake_arrow = False
            
        if first_arrow == True and 141.5689<data.pose.pose.position.x<158.4301:
            
            ShowArrow(RIGHT,1)
            first_arrow = False

        if Secound_arrow == True and 87.4309 < data.pose.pose.position.x < 93.3200:

            ShowArrow(RIGHT,2)
            Secound_arrow = False

     #if third_arrow == True and 260.0<data.pose.pose.position.x<280.0 and -3.0<data.pose.pose.position.y<-1.0: original
     #takin   if third_arrow == True and 263.5562<data.pose.pose.position.x<282.5260 and -3.0682<data.pose.pose.position.y<2.4960 :
        if third_arrow == True and 250.5562<data.pose.pose.position.x<282.5260 and -3.0682<data.pose.pose.position.y<2.4960 :

            ShowArrow(RIGHT,3)
            third_arrow = False   


        #if fourth_arrow == True and 334.0<data.pose.pose.position.x<336.0 and -80.0<data.pose.pose.position.y<-65.0: original
        if fourth_arrow == True and 334.4758<data.pose.pose.position.x<339.3086 and -80.9451<data.pose.pose.position.y<-65.6557 :
            
            ShowArrow(RIGHT,4)
            fourth_arrow = False    
            
            
        if fifth_arrow == True and 179.0041<data.pose.pose.position.x<200.0300 and -134.2839<data.pose.pose.position.y<-128.7831 :

            ShowArrow(RIGHT,5)
            fifth_arrow = False    
            
    
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
