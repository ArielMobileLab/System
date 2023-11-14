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



Agent_type = sys.argv[1]

#Agent_type = 'Face'
#Agent_type = 'Color'



pygame.init()

sound_face_1 = pygame.mixer.Sound("/home/omer/Desktop/sound/happy.mp3")
sound_face_2 = pygame.mixer.Sound("/home/omer/Desktop/sound/sad.mp3")
sound_face_3 = pygame.mixer.Sound("/home/omer/Desktop/sound/angry.mp3")


processing = False
after_hard_face = False
Start = True
Final_value_Array = []
Test = 1
Stress_Model = 1
Face_State = 1
Exit = 1
Stress_Model = 1
Mean = 1
timestamp = 0

desktop_path = os.path.expanduser('~/Desktop/Carla_Logs')

current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

file_name = os.path.join(desktop_path, 'Face_Status_{}.json'.format(current_time))


if Agent_type=='Face':
    Image_1='/home/omer/Desktop/FaceImage/1.jpeg'
    Image_1_1='/home/omer/Desktop/FaceImage/1.1.jpeg'
    Image_2='/home/omer/Desktop/FaceImage/2.jpeg'
    Image_2_2='/home/omer/Desktop/FaceImage/2.2.jpeg'
    Image_3='/home/omer/Desktop/FaceImage/3.jpeg'
    Image_3_3='/home/omer/Desktop/FaceImage/3.2.jpeg'


if Agent_type=='Color':
    Image_1='/home/omer/Desktop/ColorImage/green1.jpeg'
    Image_1_1='/home/omer/Desktop/ColorImage/green1.1.jpeg'
    Image_2='/home/omer/Desktop/ColorImage/orange1.jpeg'
    Image_2_2='/home/omer/Desktop/ColorImage/orange1.1.jpeg'
    Image_3='/home/omer/Desktop/ColorImage/red1.jpeg'
    Image_3_3='/home/omer/Desktop/ColorImage/red1.1.jpeg'



def write_to_json(data_dict):
   
    # Open the JSON file in append mode and write the data
    with open(file_name, 'a') as json_file:
        json.dump(data_dict, json_file)
        json_file.write('\n')  # Add a newline for readability




def callback(msg):
   print(msg.msg)
   global Exit
   if msg.msg == "Q pressed, exiting" or "advanceFramesAndBlockForMessages" in msg.msg:
  
    Exit = 2
    print("Exit is 2")
    try:
        plt.close('all')
    except Exception as e:
        print(e)
        sys.exit()





def GetStress(msg):


   global Final_value_Array
   global Mean
   global Stress_Model

   Final_value = math.sqrt(msg.linear_acceleration.x**2 + msg.linear_acceleration.y**2)
   #Final_value = math.sqrt(msg.linear_acceleration.x**2 + msg.linear_acceleration.y**2 + msg.linear_acceleration.z**2)
   Final_value_Array.append(Final_value)
   Final_value_Array[:] = Final_value_Array[-20:]  # Keep only the last 20 elements
   Mean =  np.average(Final_value_Array)
   Stress_Model = math.exp(0.0513 + 0.142 * math.log(Mean))





def Imege(photo_path, sec,simulation_time):

     
    timestamp = time.time() * 1000 

    Egocar_data = OrderedDict()
    Egocar_data["Type"] = "Face_Status:"
    Egocar_data["Timestamp"] = timestamp
    Egocar_data["Simulation_time"] = simulation_time
    Egocar_data["Face_State"] = Face_State

    write_to_json(Egocar_data) # for json

    plt.rcParams['toolbar'] = 'None'
    # create a figure and subplot
    fig, ax = plt.subplots(figsize=(2.3, 2.3))
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
            manager.window.wm_geometry("+3025+840")
            ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), extent=[0, 1, 0, 1], aspect='auto')
            # remove frame
            fig.canvas.manager.window.overrideredirect(1)
            # Show the plot
            plt.pause(sec)
        else:
            print("0")
    else:
        print("0")





def AgentPlot(msg):
  
   global photo
   global processing
   global after_hard_face
   global Start
   global Face_State
   global Exit
   global Stress_Model
   global timestamp

   #for log file
   simulation_time = msg.header.seq*0.033333335071821 #matlab
   #timestamp = time.time() * 1000 

   #Egocar_data = OrderedDict()
   #Egocar_data["Type"] = "Face_Status:"
   #Egocar_data["Timestamp"] = timestamp
   #Egocar_data["Simulation_time"] = simulation_time
   #Egocar_data["Face_State"] = Face_State

 
   #write_to_json(Egocar_data) # for json
   

   if Exit == 2:
                print(" go to the condition of Exit == 2")
                plt.close('all')
                print(" close")
                sys.exit()


   if not processing:

 
        processing = True

    
        # to start with image number one (2 sec)
        if Start:
            Face_State = 1
            pygame.mixer.Sound.play(sound_face_1)
            photo_path = Image_1
            sec = 2
            Imege(photo_path, sec,simulation_time)
            Start = False

        elif Face_State == 1:
            if Stress_Model > 1:
                Face_State = 2
                pygame.mixer.Sound.play(sound_face_2)
                plt.close('all')
                sec = 4
                photo_path = Image_2
                Imege(photo_path, sec,simulation_time)

            # Add more conditions as needed

        elif Face_State == 2:
            if Stress_Model > 1.3:
                Face_State = 3
                pygame.mixer.Sound.play(sound_face_3)
                plt.close('all')
                sec = 6
                photo_path = Image_3
                Imege(photo_path, sec,simulation_time)

            elif Stress_Model < 0.7 and Face_State != 3:
                pygame.mixer.Sound.play(sound_face_1)
                plt.close('all')
                Face_State = 1
                photo_path = Image_1
                sec = 1
                Imege(photo_path, sec, simulation_time)

            # Add more conditions as needed

        elif Face_State == 3:
            
            if Stress_Model < 1.2:
                pygame.mixer.Sound.play(sound_face_2)
                Face_State = 2
                plt.close('all')
                after_hard_face = True
                sec = 4
                photo_path = Image_2
                Imege(photo_path, sec,simulation_time)

            # Add more conditions as needed

        # Continue with the rest of your code...


        processing = False




# Initialize ROS node
rospy.init_node('message_listener')
matplotlib.use("TkAgg")


# Subscribe to the topic that publishes the messages from Carla
rospy.Subscriber("IMU_topic", Imu, GetStress,queue_size=1)
rospy.Subscriber("GPS_topic",NavSatFix,AgentPlot,queue_size=1)

rospy.Subscriber("/rosout", Log, callback)  # Subscribe to '/rosout' topic
# Set the desired loop frequency (1 Hz in this example)
rate = rospy.Rate(1)


# Continue running the code
while not rospy.is_shutdown():


   # if sample_rates:
   #     avg_sample_rate = sum(sample_rates) / len(sample_rates)
   #     print("Average Sample Rate:", avg_sample_rate, "Hz")
   # Sleep to maintain the desired loop frequency


   rate.sleep()

