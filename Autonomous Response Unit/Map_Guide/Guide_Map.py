

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

plt.rcParams['toolbar'] = 'None'


def ShowArrow(photo_path, sec):
    # create a figure and subplot
    fig, ax = plt.subplots(figsize=(5.5, 2.5))
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
            manager.window.wm_geometry("+2640+54")

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

    if Map_type == 'Guide_Train':

        if Brake_arrow == True:
            ShowArrow(Brake,3.5)
            Brake_arrow = False

    if Map_type == 'Guide_Spatial':
            
        if Brake_arrow == True:
            ShowArrow(Brake,3.5)
            Brake_arrow = False
            
        if first_arrow == True and 150<data.pose.pose.position.x<152:

            ShowArrow(RIGHT,sec)

            first_arrow = False

        if Secound_arrow == True and 92.0<data.pose.pose.position.x<93.0:

            ShowArrow(RIGHT,sec)
            
            Secound_arrow = False

        if third_arrow == True and 260.0<data.pose.pose.position.x<280.0 and -3.0<data.pose.pose.position.y<-1.0:

            ShowArrow(RIGHT,sec)
            
            third_arrow = False    
            
        
        if fourth_arrow == True and 334.0<data.pose.pose.position.x<336.0 and -80.0<data.pose.pose.position.y<-40.0:

            ShowArrow(RIGHT,sec)
            
            fourth_arrow = False    
            
            
        if fifth_arrow == True and 195.293121338<data.pose.pose.position.x<200.00000 and -131.0<data.pose.pose.position.y<-128.0 :

            ShowArrow(RIGHT,sec)
            
            fifth_arrow = False    
            
    
 	    
	
    

# Initialize ROS node
rospy.init_node('Arrow_Guide')
matplotlib.use("TkAgg")

rospy.Subscriber('Odomerty_topic',Odometry, Arrows, queue_size=1)  

rate = rospy.Rate(1)


# Continue running the code
while not rospy.is_shutdown():


   # if sample_rates:
   #     avg_sample_rate = sum(sample_rates) / len(sample_rates)
   #     print("Average Sample Rate:", avg_sample_rate, "Hz")
   # Sleep to maintain the desired loop frequency


   rate.sleep()

