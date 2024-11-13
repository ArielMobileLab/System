#!/usr/bin/env python


import subprocess
from cognata_api.web_api.cognata_demo import CognataRequests as cog_api
import time
import os
import threading
import queue
import timeit
import signal
from contextlib import contextmanager
import sys
import json
import keyboard
import rospy
import tkinter as tk
from tkinter import messagebox
from geometry_msgs.msg import Point
from std_msgs.msg import Float64
from sensor_msgs.msg import NavSatFix
from tkinter import ttk
from PIL import Image, ImageTk
import vlc
import subprocess
import webbrowser


import os

def play_video(video_path):
    
    # video_x = 1920 * 2  # Adjust this value to match the screen width of your setup
    # video_y = 0        # Adjust this value to match the screen height and positioning of your setup
    subprocess.Popen(['vlc',video_path,'--fullscreen','--play-and-exit']) 

def open_url(url):
    webbrowser.open(url)



# Create the root window
root = tk.Tk()
s = ttk.Style()
root.title("MobileLab Scenario Menu")
root.geometry("1920x1080")

# Use the Clam theme
s.theme_use('clam')
s.configure("Custom.TButton", padding=20, font=("Tahoma", 12))

files = os.listdir("/dev/input/by-id/")

wheelName = 'null'
# Iterate over the list of files
for file in files:
    # Check if the file name contains the string "Wheel-event-joystick"
    if "-event-joystick" in file:
        wheelName = file


# Create a function to launch the selected scenario
def launch_scenario(scenarioslist,Town,Face,Objects, Arrow_Guilde, Delay, Gap, Agent, Predictive_Display):
    if wheelName != 'null':
        os.system('ffset /dev/input/by-id/' + wheelName + ' -a 50')
    for scenario in scenarioslist:
        root.withdraw()  # added this line to hide the root window
        repeat = 1
        while repeat == 1:
            try:

                # Use subprocess to execute the command,  # Agent is tele assite or tele driving
                subprocess.run(["bash", scenario, Town, Face, Objects, Arrow_Guilde, Delay, Gap, Agent, Predictive_Display], check=True)
                repeat = 0
            except subprocess.CalledProcessError:
                repeat = 1

        if repeat == 0:
            root.deiconify()
            root.update()



# Create a list of scenarios

scenarios = [
    {
        "name": "Training-Joystic (For Tele-Driving)",
        "description": "",
        "video_path": "/home/omer/Desktop/Experiment Managment Unit/Simulations/Main_Menu Videos/Tele_assist_Tele_Driving/Joy_Train.MOV", 
        "NASA": "https://docs.google.com/forms/d/e/1FAIpQLSfGy6BIwAGpHZDJ-Uk6T1q9awHvASKNafpMJdrHi8HLvBCeOg/viewform",
        "code": ["//home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/Train_first_respons.sh","Town02","Teledriving_Train_1","Nah","Guide_Train", "0", "0", "tele_driving", "Predictive_OFF"],
        "code1": ["//home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/Train_first_respons.sh","Town02","Teledriving_Train_1","Nah","Guide_Train", "0", "0", "tele_driving", "Predictive_OFF"],
    },
     {
        "name": "Training",
        "description": "",
        "video_path": "/home/omer/Desktop/Experiment Managment Unit/Simulations/Main_Menu Videos/Tele_assist_Tele_Driving/Tele_Driving_Train_PD.MOV", 
        "video_path1": "/home/omer/Desktop/Experiment Managment Unit/Simulations/Main_Menu Videos/Tele_assist_Tele_Driving/Tele_Assist_Train.MOV",
        "NASA": "https://docs.google.com/forms/d/e/1FAIpQLSfGy6BIwAGpHZDJ-Uk6T1q9awHvASKNafpMJdrHi8HLvBCeOg/viewform",
        "code": ["//home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/Train_first_respons_2.sh","Town04","Teledriving_Train_2","Nah","First_Response_train_2", "50", "0", "tele_driving", "Predictive_ON"],
        "code1": ["//home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/Train_first_respons_2_assit.sh","Town04","Teledriving_Train_2","Nah","First_Response_train_2", "50", "0", "tele_driving", "Predictive_OFF"],
    },
    {
        "name": "Tele_assist",
        "description": "",
        "video_path": "/home/omer/Desktop/Experiment Managment Unit/Simulations/Main_Menu Videos/Tele_assist_Tele_Driving/Tele_Assist.MOV",
        "NASA1": "https://docs.google.com/forms/d/e/1FAIpQLSfx4wrdAquDLUB-hKgwHPeI9ikIynPzvf-pvr3FSruK1RQASA/viewform",
	    "NASA2": "https://docs.google.com/forms/d/e/1FAIpQLSfGy6BIwAGpHZDJ-Uk6T1q9awHvASKNafpMJdrHi8HLvBCeOg/viewform",
        "code": ["/home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders_assist.sh","Town04","Teleassiste_50_Easy","Nah","First_Response","50", "0", "tele_assiste", "Predictive_OFF"],
        "code1": ["/home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders_assist.sh","Town04","Teleassiste_150_Hard","Nah","First_Response","150", "1", "tele_assiste", "Predictive_OFF"],
        "code2": ["//home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders_assist.sh","Town04","Teleassiste_50_Hard","Nah","First_Response", "50", "1", "tele_assiste", "Predictive_OFF"],
        "code3": ["//home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders_assist.sh","Town04","Teleassiste_150_Easy","Nah","First_Response", "150", "0", "tele_assiste", "Predictive_OFF"],
    },
    {
        "name": "Tele_driving ",
        "description": "",
        "video_path": "/home/omer/Desktop/Experiment Managment Unit/Simulations/Main_Menu Videos/Tele_assist_Tele_Driving/Tele_Driving.MOV",
        "NASA1": "https://docs.google.com/forms/d/e/1FAIpQLSfx4wrdAquDLUB-hKgwHPeI9ikIynPzvf-pvr3FSruK1RQASA/viewform",
	    "NASA2": "https://docs.google.com/forms/d/e/1FAIpQLSfGy6BIwAGpHZDJ-Uk6T1q9awHvASKNafpMJdrHi8HLvBCeOg/viewform",
        "code": ["/home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders.sh","Town04","Teledriving_50_Easy","Nah","First_Response","50", "0", "tele_driving", "Predictive_OFF"],
        "code1": ["/home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders.sh","Town04","Teledriving_150_Hard","Nah","First_Response","150", "1", "tele_driving", "Predictive_OFF"],
        "code2": ["/home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders.sh","Town04","Teledriving_50_Hard","Nah","First_Response", "50", "1", "tele_driving", "Predictive_OFF"],
        "code3": ["/home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders.sh","Town04","Teledriving_150_Easy","Nah","First_Response", "150", "0", "tele_driving", "Predictive_OFF"]
    },
    {
        "name": "Tele_driving + P.D",
        "description": "",
        "video_path": "/home/omer/Desktop/Experiment Managment Unit/Simulations/Main_Menu Videos/Tele_assist_Tele_Driving/Tele_Driving_PD.MOV",
        "NASA1": "https://docs.google.com/forms/d/e/1FAIpQLSfx4wrdAquDLUB-hKgwHPeI9ikIynPzvf-pvr3FSruK1RQASA/viewform",
	    "NASA2": "https://docs.google.com/forms/d/e/1FAIpQLSfGy6BIwAGpHZDJ-Uk6T1q9awHvASKNafpMJdrHi8HLvBCeOg/viewform",
        "code": ["/home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders.sh","Town04","Teledriving_50_Easy","Nah","First_Response","50", "0", "tele_driving", "Predictive_ON"],
        "code1": ["/home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders.sh","Town04","Teledriving_150_Hard","Nah","First_Response","150", "1", "tele_driving", "Predictive_ON"],
        "code2": ["/home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders.sh","Town04","Teledriving_50_Hard","Nah","First_Response", "50", "1", "tele_driving", "Predictive_ON"],
        "code3": ["/home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/First_Responders.sh","Town04","Teledriving_150_Easy","Nah","First_Response", "150", "0", "tele_driving", "Predictive_ON"]
    },
    {
        "name": "Regual_City",
        "description": "",
        "video_path": "/home/omer/Desktop/Experiment Managment Unit/Simulations/Main_Menu Videos/Tele_assist_Tele_Driving/Reg_Latency.MOV",
	"video_path1": "/home/omer/Desktop/Experiment Managment Unit/Simulations/Main_Menu Videos/Tele_assist_Tele_Driving/Reg_Latancy_PD.MOV",
        "NASA": "https://docs.google.com/forms/d/e/1FAIpQLSfGy6BIwAGpHZDJ-Uk6T1q9awHvASKNafpMJdrHi8HLvBCeOg/viewform",
        "code": ["//home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/Regular_A.sh","Town01","Regular_50","Obstacle_A","Guide_Parent", "50", "0", "tele_driving", "Predictive_ON"],
        "code1": ["//home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/Regular_A.sh","Town01","Regular_150","Obstacle_A","Guide_Parent", "150", "0", "tele_assist", "Predictive_ON"],   
        "code2": ["//home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/Regular_A_PD.sh","Town01","Regular_50 + PD","Obstacle_A","Guide_Parent", "50", "0", "tele_assist", "Predictive_OFF"],
        "code3": ["//home/omer/Desktop/Experiment Managment Unit/Simulations/Carla/First_Responders/Senarios/Regular_A_PD.sh","Town01","Regular_150 + PD","Obstacle_A","Guide_Parent", "150", "0", "tele_assist", "Predictive_OFF"]
    }
]




# Create a function to display the scenario menu
def show_scenario_menu():
    # Create a label with the big title
    big_title_label = tk.Label(root, text="Welcome to MobileLab Scenario Menu", font=("Tahoma", 38, "bold"))
    big_title_label.pack(pady=20)

    # Create a label with the smaller title
    small_title_label = tk.Label(root, text="Please choose a scenario", font=("Tahoma", 31))
    small_title_label.pack()

   
    # Create buttons for each scenario
    for scenario in scenarios:
	    
	
        # Create a frame to hold the scenario information
        scenario_frame = tk.Frame(root, bg="black", padx=10, pady=10)
        scenario_frame.pack(pady=15, anchor="w", fill="x")

        if scenario["name"] == "Regual_City":

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" 50ms", command=lambda s=scenario: launch_scenario(s["code"] ,s["code"][1],s["code"][2],s["code"][3],s["code"][4],s["code"][5],s["code"][6],s["code"][7],s["code"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure()
            scenario_button.pack(side=tk.RIGHT)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" 150ms", command=lambda s=scenario: launch_scenario(s["code1"] ,s["code1"][1],s["code1"][2],s["code1"][3],s["code1"][4],s["code1"][5],s["code1"][6],s["code1"][7],s["code1"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure()
            scenario_button.pack(side=tk.RIGHT)


        # Create a play video button
            play_video_button = ttk.Button(scenario_frame, text="Video P.D", command=lambda url=scenario["video_path1"]: play_video(url))
            play_video_button.configure()
            play_video_button.pack(side=tk.RIGHT, padx=5)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" 50ms + P.D ", command=lambda s=scenario: launch_scenario(s["code2"] ,s["code2"][1],s["code2"][2],s["code2"][3],s["code2"][4],s["code2"][5],s["code2"][6],s["code2"][7],s["code2"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure()
            scenario_button.pack(side=tk.RIGHT)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" 150ms + P.D", command=lambda s=scenario: launch_scenario(s["code3"] ,s["code3"][1],s["code3"][2],s["code3"][3],s["code3"][4],s["code3"][5],s["code3"][6],s["code3"][7],s["code3"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure()
            scenario_button.pack(side=tk.RIGHT)
        # Create a play video button
            play_video_button = ttk.Button(scenario_frame, text="Video", command=lambda url=scenario["video_path"]: play_video(url))
            play_video_button.configure()
            play_video_button.pack(side=tk.RIGHT, padx=5)
            
        elif scenario["name"] == "Tele_driving + P.D":
            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" Hard 50ms ", command=lambda s=scenario: launch_scenario(s["code"] ,s["code"][1],s["code"][2],s["code"][3],s["code"][4],s["code"][5],s["code"][6],s["code"][7],s["code"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" Easy 150ms", command=lambda s=scenario: launch_scenario(s["code1"] ,s["code1"][1],s["code1"][2],s["code1"][3],s["code1"][4],s["code1"][5],s["code1"][6],s["code1"][7],s["code1"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" Easy 50ms", command=lambda s=scenario: launch_scenario(s["code2"] ,s["code2"][1],s["code2"][2],s["code2"][3],s["code2"][4],s["code2"][5],s["code2"][6],s["code2"][7],s["code1"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" Hard 150ms", command=lambda s=scenario: launch_scenario(s["code3"] ,s["code3"][1],s["code3"][2],s["code3"][3],s["code3"][4],s["code3"][5],s["code3"][6],s["code3"][7],s["code1"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

        # Create a play video button
            play_video_button = ttk.Button(scenario_frame, text="video", command=lambda url=scenario["video_path"]: play_video(url))
            play_video_button.configure(style="Custom.TButton")
            play_video_button.pack(side=tk.RIGHT, padx=5)



        elif scenario["name"] == "Training":
       # Create a scenario button
            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" tele_driving P.D", command=lambda s=scenario: launch_scenario(s["code"] ,s["code"][1],s["code"][2],s["code"][3],s["code"][4],s["code"][5],s["code"][6],s["code"][7],s["code"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

       # Create a play video button
            play_video_button = ttk.Button(scenario_frame, text="Video driving", command=lambda url=scenario["video_path"]: play_video(url))
            play_video_button.configure(style="Custom.TButton")
            play_video_button.pack(side=tk.RIGHT, padx=5)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" tele_assist ", command=lambda s=scenario: launch_scenario(s["code1"] ,s["code1"][1],s["code1"][2],s["code1"][3],s["code1"][4],s["code1"][5],s["code1"][6],s["code1"][7],s["code1"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

       # Create a play video button
            play_video_button = ttk.Button(scenario_frame, text="Video assit", command=lambda url=scenario["video_path"]: play_video(url))
            play_video_button.configure(style="Custom.TButton")
            play_video_button.pack(side=tk.RIGHT, padx=5)





        elif scenario["name"] ==  scenario["name"] == "Training-Joystic (For Tele-Driving)" or scenario["name"] == "Training-tele-asist" :
            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text="Scenario 50ms", command=lambda s=scenario: launch_scenario(s["code"] ,s["code"][1],s["code"][2],s["code"][3],s["code"][4],s["code"][5],s["code"][6],s["code"][7],s["code1"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)


            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text="Scenario 150ms", command=lambda s=scenario: launch_scenario(s["code1"] ,s["code1"][1],s["code1"][2],s["code1"][3],s["code1"][4],s["code1"][5],s["code1"][6],s["code1"][7],s["code1"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)


        else:   
            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" Hard 50ms ", command=lambda s=scenario: launch_scenario(s["code"] ,s["code"][1],s["code"][2],s["code"][3],s["code"][4],s["code"][5],s["code"][6],s["code"][7],s["code"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" Easy 150ms", command=lambda s=scenario: launch_scenario(s["code1"] ,s["code1"][1],s["code1"][2],s["code1"][3],s["code1"][4],s["code1"][5],s["code1"][6],s["code1"][7],s["code1"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" Easy 50ms", command=lambda s=scenario: launch_scenario(s["code2"] ,s["code2"][1],s["code2"][2],s["code2"][3],s["code2"][4],s["code2"][5],s["code2"][6],s["code2"][7],s["code1"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text=" Hard 150ms", command=lambda s=scenario: launch_scenario(s["code3"] ,s["code3"][1],s["code3"][2],s["code3"][3],s["code3"][4],s["code3"][5],s["code3"][6],s["code3"][7],s["code1"][8]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

        # Create a play video button
            play_video_button = ttk.Button(scenario_frame, text="Video", command=lambda url=scenario["video_path"]: play_video(url))
            play_video_button.configure(style="Custom.TButton")
            play_video_button.pack(side=tk.RIGHT, padx=5)

            





    

        # Create a frame for the description label
        description_frame = tk.Frame(scenario_frame, bg="black")
        description_frame.pack(side=tk.LEFT, padx=10, fill="both", expand=True)

        s.configure("Danger.TButton", foreground="Black", background="green", padding=(20, 15), font=("Tahoma", 14, "bold"))     

       

        # Create a label with the scenario description
        title_label = tk.Label(description_frame, text=scenario["name"], font=("Tahoma", 13, "bold"), wraplength=600,width=28, fg="white", bg="black",anchor="w")
        title_label.grid(row=0, column=0, padx=4, pady=5, sticky="w")

        # Create a label with the scenario description
        description_label = tk.Label(description_frame, text=scenario["description"], font=("Tahoma", 13),width=70, wraplength=780, fg="white", bg="black")
        description_label.grid(row=0, column=1,columnspan=2, padx=1, pady=1)

        # Configure the grid columns to center-align the labels
        title_label.columnconfigure(0, weight=1)
        description_frame.columnconfigure(1, weight=1)


    frame = tk.Frame(root, bg="black", padx=10, pady=10)
    frame.pack(pady=15, anchor="w", fill="x")




# Show the initial scenario menu
show_scenario_menu()

# Run the main loop
root.mainloop()


# OnLy GoD cAn judGe mE
