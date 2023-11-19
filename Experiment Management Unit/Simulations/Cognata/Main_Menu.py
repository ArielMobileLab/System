import subprocess
import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import vlc
import webbrowser

root = tk.Tk()
s = ttk.Style()
root.title("MobileLab Scenario Menu")
root.geometry("1920x1080")

s.theme_use('clam')
s.configure("Custom.TButton", padding=12, font=("Tahoma", 12))
s.configure("Smaller.TButton", padding=13, font=("Tahoma", 12))

files = os.listdir("/dev/input/by-id/")
wheelName = 'null'

for file in files:
    if "-event-joystick" in file:
        wheelName = file

def play_video(video_path):
    subprocess.Popen(['vlc', video_path, '--fullscreen', '--play-and-exit']) 

def launch_scenario(scenarioslist):
    if wheelName != 'null':
        os.system('ffset /dev/input/by-id/' + wheelName + ' -a 30')
    
    for scenario in scenarioslist:
        root.withdraw()
        for command in scenario:
            repeat = True
            while repeat:
                os.system(command)
                if subprocess.call(["pgrep", "-f", "SimCloud"]) == 0: #If you detect an exit from cognata
                    repeat = messagebox.askyesno("Warning", "Repeat?") 
                    if not repeat:
                        root.update()
                        break  # Exit the while loop if repeat is False
                    root.update()
                else: #If cognata simulator failed to load up break the loop
                    break    


        root.deiconify()
        root.update()
                    

# def reload(x):

#     if wheelName != 'null':
#         os.system('ffset /dev/input/by-id/' + wheelName + ' -a 30')
#     repeat = 1
#     while repeat == 1:
#         os.system(x)
#         if 'kill -9 $(ps -e | grep SimCloud | head -c 6)':
#             repeat = messagebox.askyesno("Warning", "Repeat?")
#         if repeat == 0:
#             root.update()
#             break
#         root.update()
#         root.withdraw()  # added this line to hide the root windowsa

scenarios = [
    {
        "name": "Training",
        "description": "Get used to driving with our steering wheel and brakes in an urban scenario",
        "video_path": "./videos/Training.mp4",
        "buttons_names": ["Go to Scenario"],
        "code": [[
            "python3 adaptiveTraining.py train CarControl_0_0 allocentric-rear"
            ]]
    },
    {
        "name": "Load-Car1",
        "description": "In this scenario you will experience communication time delay while driving after a lead vehicle (black car) - think you can teleoperate safely",
        "video_path": "./videos/ACC semantic.mp4",
        "buttons_names": ["50ms ML", "150ms ML", "50ms 15m", "150ms 15m", "250ms 15m", "250ms ML"],
        "code": [     
            #1     
            ["python3 adaptiveTraining.py load-1 CarControl_50_Matlab allocentric-rear"],
            #2
            ["python3 adaptiveTraining.py load-1 CarControl_150_Matlab allocentric-rear"],
            #3
            ["python3 adaptiveTraining.py load-1 CarControl_50_15 allocentric-rear"],
            #4
            ["python3 adaptiveTraining.py load-1 CarControl_150_15 allocentric-rear"], 
	    #5 
	    ["python3 adaptiveTraining.py load-1 CarControl_250_15 allocentric-rear"], 	 
            #6
	    ["python3 adaptiveTraining.py load-1 CarControl_250_Matlab allocentric-rear"] 	                      
            ]
    },
{
        "name": "Load-Car2",
        "description": "In this scenario you will experience communication time delay while driving after a lead vehicle (black car) - think you can teleoperate safely",
        "video_path": "./videos/ACC semantic.mp4",
        "buttons_names": ["50ms ML", "150ms ML", "50ms 15m", "150ms 15m", "250ms 15m", "250ms ML"],
        "code": [     
            #1     
            ["python3 adaptiveTraining.py load-2 CarControl_50_Matlab allocentric-rear"],
            #2
            ["python3 adaptiveTraining.py load-2 CarControl_150_Matlab allocentric-rear"],
            #3
            ["python3 adaptiveTraining.py load-2 CarControl_50_15 allocentric-rear"],
            #4
            ["python3 adaptiveTraining.py load-2 CarControl_150_15 allocentric-rear"],  
            #5 
	    ["python3 adaptiveTraining.py load-2 CarControl_250_15 allocentric-rear"], 	 
            #6
	    ["python3 adaptiveTraining.py load-2 CarControl_250_Matlab allocentric-rear"] 	                                                        
            ]
    },
{
        "name": "Load-Car3",
        "description": "In this scenario you will experience communication time delay while driving after a lead vehicle (black car) - think you can teleoperate safely",
        "video_path": "./videos/ACC semantic.mp4",
        "buttons_names": ["50ms ML", "150ms ML", "50ms 15m", "150ms 15m", "250ms 15m", "250ms ML"],
        "code": [     
            #1     
            ["python3 adaptiveTraining.py load-3 CarControl_50_Matlab allocentric-rear"],
            #2
            ["python3 adaptiveTraining.py load-3 CarControl_150_Matlab allocentric-rear"],
            #3
            ["python3 adaptiveTraining.py load-3 CarControl_50_15 allocentric-rear"],
            #4
            ["python3 adaptiveTraining.py load-3 CarControl_150_15 allocentric-rear"],
            #5 
	    ["python3 adaptiveTraining.py load-3 CarControl_250_15 allocentric-rear"], 	 
            #6
	    ["python3 adaptiveTraining.py load-3 CarControl_250_Matlab allocentric-rear"]                                     
            ]
    },
    {
        "name": "Load-Cube",
        "description": "To ease communication time delay, the teleoperation system, uses semantic representation of cars. In addition to the time delay,  you will see bounding boxes instead of cars. Think you can handle this one",
        "video_path": "./videos/ACC semantic.mp4",
        "buttons_names": ["50ms ML", "150ms ML", "50ms 15m", "150ms 15m", "250ms 15m", "250ms ML"],
        "code": [#1
                ["python3 adaptiveTraining.py load2_cube CarControl_50_Matlab allocentric-rear"],
                 #2
                 ["python3 adaptiveTraining.py load2_cube CarControl_150_Matlab allocentric-rear"],
                 #3
                 ["python3 adaptiveTraining.py load2_cube CarControl_50_15 allocentric-rear"],
                 #4
                 ["python3 adaptiveTraining.py load2_cube CarControl_150_15 allocentric-rear"],
                 #5 
	         ["python3 adaptiveTraining.py load2_cube CarControl_250_15 allocentric-rear"], 	 
                 #6
	         ["python3 adaptiveTraining.py load2_cube CarControl_250_Matlab allocentric-rear"]    
]
    },
    {
        "name": "Spatial",
        "description": "Drive around the city while  following the instruction signs Use regular driver viewpoint",
        "video_path": "./videos/Allocentric.mp4",
        "buttons_names": ["Allo", "Ego"],
        "code": [
                 #ALO
                 ["python3 adaptiveTraining.py spatial CarControl_0_0 allocentric"],
                 #EGO
                 ["python3 adaptiveTraining.py spatial CarControl_0_0 egocentric"]]
    }
   

]



def show_scenario_menu():
    big_title_label = tk.Label(root, text="Welcome to MobileLab Scenario Menu", font=("Tahoma", 20, "bold"))
    big_title_label.pack(pady=20)

    small_title_label = tk.Label(root, text="Please choose a scenario", font=("Tahoma", 20))
    small_title_label.pack()

    for scenario in scenarios:
        scenario_frame = tk.Frame(root, bg="black", padx=10, pady=10)
        scenario_frame.pack(pady=15, anchor="w", fill="x")

        description_frame = tk.Frame(scenario_frame, bg="black")
        description_frame.pack(side=tk.LEFT, padx=10, fill="both", expand=True)

        title_label = tk.Label(description_frame, text=scenario["name"], font=("Tahoma", 16, "bold"), wraplength=300, width=28, fg="white", bg="black", anchor="w")
        title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        if "description" in scenario:
            description_label = tk.Label(description_frame, text=scenario["description"], font=("Tahoma", 15), width=70, wraplength=780, fg="white", bg="black")
            description_label.grid(row=0, column=1, columnspan=2, padx=1, pady=1)

        title_label.columnconfigure(0, weight=1)
        description_frame.columnconfigure(1, weight=1)

        custom_style = ttk.Style()
        custom_style.configure("Custom.TButton", font=("Helvetica", 8), padding=7)

        play_video_button = ttk.Button(scenario_frame, text="Play Video", command=lambda url=scenario["video_path"]: play_video(url))
        play_video_button.configure(style="Custom.TButton")
        play_video_button.pack(side=tk.RIGHT, padx=5)

     

        buttons_frame = tk.Frame(scenario_frame, bg="black")
        buttons_frame.pack(side=tk.RIGHT)

        num_buttons = len(scenario["buttons_names"])
        num_rows = (num_buttons + 1) // 2  # Calculate number of rows (rounded up)

        for i, button_name in enumerate(scenario["buttons_names"]):
            index = i  # Index variable to track the current index in the code array
            scenario_button = ttk.Button(buttons_frame, text=button_name, command=lambda s=scenario, i=index: launch_scenario([s["code"][i]]))
            scenario_button.configure(style="Custom.TButton")
            row = i // 2  # Calculate row index
            col = i % 2   # Calculate column index
            scenario_button.grid(row=row, column=col, padx=5, pady=5)



show_scenario_menu()
root.mainloop()

