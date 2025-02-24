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
def launch_scenario(scenarioslist,Town,Face,Objects, Arrow_Guilde,Senario_type):
    if wheelName != 'null':
        os.system('ffset /dev/input/by-id/' + wheelName + ' -a 50')
    for scenario in scenarioslist:
        root.withdraw()  # added this line to hide the root window
        repeat = 1
        while repeat == 1:
            try:

                # Use subprocess to execute the command
                subprocess.run(["bash", scenario, Town, Face, Objects, Arrow_Guilde,Senario_type], check=True)
                repeat = 0
            except subprocess.CalledProcessError:
                repeat = 1

        if repeat == 0:
            root.deiconify()
            root.update()



# Create a list of scenarios

scenarios = [

    {
        "name": "Training",
        "description": "",
        "video_path": "/home/omer/Desktop/Experiment Management Unit/Simulations/Main_Menu Videos/Parent/Train_Parent.mp4", 
        "NASA": "https://docs.google.com/forms/d/e/1FAIpQLSfGy6BIwAGpHZDJ-Uk6T1q9awHvASKNafpMJdrHi8HLvBCeOg/viewform",
        "code": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Accompanying_expiriment/Senarios/Train_parent.sh","Town02","Training","Train","Guide_Train","1"]
    },
    {
        "name": "Far",
        "description": "",
        "video_path": "/home/omer/Desktop/Experiment Management Unit/Simulations/Main_Menu Videos/Parent/Parent_Driver_From_Far.mp4", 
        "NASA": "https://docs.google.com/forms/d/e/1FAIpQLSfGy6BIwAGpHZDJ-Uk6T1q9awHvASKNafpMJdrHi8HLvBCeOg/viewform",
        "code": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Accompanying_expiriment/Senarios/Parent_with_out_videos_A.sh","Town01","Simulation_Far_MapA","Simulation_Far_MapA","Guide_Parent","2"],
	"code1": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Accompanying_expiriment/Senarios/Parent_with_out_videos_B.sh","Town01","Simulation_Far_MapB","Simulation_Far_MapB","Guide_Parent","3"],
        "code2": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Accompanying_expiriment/Senarios/Parent_with_out_videos_C.sh","Town01","Simulation_Far_MapC","Simulation_Far_MapC","Guide_Parent_C","4"],
    },
    {
        "name": "Close",
        "description": "",
        "video_path": "/home/omer/Desktop/Experiment Management Unit/Simulations/Main_Menu Videos/Parent/Driver_Side_Close.mp4", 
        "NASA": "https://docs.google.com/forms/d/e/1FAIpQLSfGy6BIwAGpHZDJ-Uk6T1q9awHvASKNafpMJdrHi8HLvBCeOg/viewform",
        "code": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Accompanying_expiriment/Senarios/Parent_with_out_videos_A.sh","Town01","Simulation_Close_MapA","Simulation_Close_MapA","Guide_Parent","5"],
	"code1": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Accompanying_expiriment/Senarios/Parent_with_out_videos_B.sh","Town01","Simulation_Close_MapB","Simulation_Close_MapB","Guide_Parent","6"],
        "code2": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Accompanying_expiriment/Senarios/Parent_with_out_videos_C.sh","Town01","Simulation_Close_MapC","Simulation_Close_MapC","Guide_Parent_C","7"],
    },
    {
        "name": "Avatar",
        "description": "",
        "video_path": "/home/omer/Desktop/Experiment Management Unit/Simulations/Main_Menu Videos/Parent/Driver_Side_with_Avatar.mp4", 
        "NASA": "https://docs.google.com/forms/d/e/1FAIpQLSfGy6BIwAGpHZDJ-Uk6T1q9awHvASKNafpMJdrHi8HLvBCeOg/viewform",
        "code": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Accompanying_expiriment/Senarios/Parent_videos_A.sh","Town01","Simulation_Avatar_MapA","Simulation_Avatar_MapA","Guide_Parent","8"],
	"code1": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Accompanying_expiriment/Senarios/Parent_videos_B.sh","Town01","Simulation_Avatar_MapB","Simulation_Avatar_MapB","Guide_Parent","9"],
        "code2": ["/home/omer/Desktop/Experiment Management Unit/Simulations/Carla/Accompanying_expiriment/Senarios/Parent_videos_C.sh","Town01","Simulation_Avatar_MapC","Simulation_Avatar_MapC","Guide_Parent_C","10"],
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

        if scenario["name"] == "Training":
            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text="Scenario", command=lambda s=scenario: launch_scenario(s["code"] ,s["code"][1],s["code"][2],s["code"][3],s["code"][4],s["code"][5]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

        else:   
            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text="Scenario A", command=lambda s=scenario: launch_scenario(s["code"] ,s["code"][1],s["code"][2],s["code"][3],s["code"][4],s["code"][5]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text="Scenario B", command=lambda s=scenario: launch_scenario(s["code1"] ,s["code1"][1],s["code1"][2],s["code1"][3],s["code1"][4],s["code1"][5]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

            # Create a scenario button
            scenario_button = ttk.Button(scenario_frame, text="Scenario C", command=lambda s=scenario: launch_scenario(s["code2"] ,s["code2"][1],s["code2"][2],s["code2"][3],s["code2"][4],s["code2"][5]))
            #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
            scenario_button.configure(style="Custom.TButton")
            scenario_button.pack(side=tk.RIGHT)

    

    

        # Create a frame for the description label
        description_frame = tk.Frame(scenario_frame, bg="black")
        description_frame.pack(side=tk.LEFT, padx=10, fill="both", expand=True)

        s.configure("Danger.TButton", foreground="Black", background="green", padding=(20, 15), font=("Tahoma", 14, "bold"))     

       

        # Create a label with the scenario description
        title_label = tk.Label(description_frame, text=scenario["name"], font=("Tahoma", 16, "bold"), wraplength=300,width=28, fg="white", bg="black",anchor="w")
        title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Create a label with the scenario description
        description_label = tk.Label(description_frame, text=scenario["description"], font=("Tahoma", 13),width=70, wraplength=780, fg="white", bg="black")
        description_label.grid(row=0, column=1,columnspan=2, padx=1, pady=1)

        # Configure the grid columns to center-align the labels
        title_label.columnconfigure(0, weight=1)
        description_frame.columnconfigure(1, weight=1)

        # Create a play video button
        play_video_button = ttk.Button(scenario_frame, text="Video", command=lambda url=scenario["video_path"]: play_video(url))
        play_video_button.configure(style="Custom.TButton")
        play_video_button.pack(side=tk.RIGHT, padx=5)


    frame = tk.Frame(root, bg="black", padx=10, pady=10)
    frame.pack(pady=15, anchor="w", fill="x")




# Show the initial scenario menu
show_scenario_menu()

# Run the main loop
root.mainloop()

