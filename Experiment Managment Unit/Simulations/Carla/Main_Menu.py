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
def launch_scenario(scenarioslist,Town,Face,Objects, Arrow_Guilde):
    if wheelName != 'null':
        os.system('ffset /dev/input/by-id/' + wheelName + ' -a 30')
    for scenario in scenarioslist:
        root.withdraw()  # added this line to hide the root window
        repeat = 1
        while repeat == 1:
            try:

                # Use subprocess to execute the command
                subprocess.run(["bash", scenario, Town, Face, Objects, Arrow_Guilde], check=True)
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
        "description": "Get used to driving with our steering wheel and brakes in an urban scenario",
        "video_path": "./videos/Training.mp4", 
        "code": ["/home/omer/Desktop/CARLA_0.9.13/Main_menu/startScenarioTrain.sh","Town05","No_Face","Train","Guide_Train"]
    },
    {
        "name": "Face",
        "description": "Drive around the city whole following the instruction signs with Face Agent ",
        "video_path": "./videos/Face.mp4",
        "code": ["/home/omer/Desktop/CARLA_0.9.13/Main_menu/startScenarioSpatial.sh","Town01","Face","Spatial","Guide_Spatial"]
    },
    {
        "name": "Color",
        "description": "Drive around the city whole following the instruction signs with Color Agent",
        "video_path": "./videos/Color.mp4",
        "code": ["/home/omer/Desktop/CARLA_0.9.13/Main_menu/startScenarioSpatial.sh","Town01","Color","Spatial","Guide_Spatial"]
    },
    {
        "name": "No_Face",
        "description": "Drive around the city whole following the instruction signs",
        "video_path": "./videos/None.mp4",
        "code": ["/home/omer/Desktop/CARLA_0.9.13/Main_menu/startScenarioSpatial.sh","Town01","No_Face","Spatial","Guide_Spatial"]
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

        # Create a scenario button
        scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"] ,s["code"][1],s["code"][2],s["code"][3],s["code"][4]))
        #scenario_button = ttk.Button(scenario_frame, text="Go to Scenario", command=lambda s=scenario: launch_scenario(s["code"],s["Town"]))
        scenario_button.configure(style="Custom.TButton")
        scenario_button.pack(side=tk.RIGHT)

        # Create a frame for the description label
        description_frame = tk.Frame(scenario_frame, bg="black")
        description_frame.pack(side=tk.LEFT, padx=10, fill="both", expand=True)

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
        play_video_button = ttk.Button(scenario_frame, text="Play Video", command=lambda url=scenario["video_path"]: play_video(url))
        play_video_button.configure(style="Custom.TButton")
        play_video_button.pack(side=tk.RIGHT, padx=5)

# Show the initial scenario menu
show_scenario_menu()

# Run the main loop
root.mainloop()


# OnLy GoD cAn judGe mE
