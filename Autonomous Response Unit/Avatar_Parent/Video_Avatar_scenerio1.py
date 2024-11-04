import rospy
from nav_msgs.msg import Odometry
import vlc
import time
import tkinter as tk
import json

# Global flags to track if the videos have been played
video_flags = {
    'video1': False,
    'video2': False,
    'video3': False,
    'video4': False,
    'video5': False
}

folder_path = "/home/omer/Desktop/Carla_Logs/Logs"
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
file_name = os.path.join(folder_path, 'Video_Status{}_{}.json'.format(Agent_type, current_time))

def play_video(video_path, window_x, window_y, window_width, window_height):
    # Create a Tkinter window
    root = tk.Tk()
    root.geometry("{0}x{1}+{2}+{3}".format(window_width, window_height, window_x, window_y))
    root.title("Video Player")

    # Initialize VLC player
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(video_path)
    player.set_media(media)

    # Embed VLC player in Tkinter window
    root.update()
    player.set_xwindow(root.winfo_id())

    # Play the video
    player.play()

    # Wait for a short time to let the player start
    time.sleep(1)

    # Check if the video is still playing
    def check_video():
        if player.get_state() not in (vlc.State.Ended, vlc.State.Error):
            root.after(100, check_video)
        else:
            root.destroy()

    root.after(100, check_video)
    root.mainloop()



def write_to_json(data_dict):
   
    # Open the JSON file in append mode and write the data
    with open(file_name, 'a') as json_file:
        json.dump(data_dict, json_file)
        json_file.write('\n')  # Add a newline for readability


def odometry_callback(data):
    global video_flags
    print("hii")

    x = data.pose.pose.position.x
    y = data.pose.pose.position.y

    # Screen dimensions
    single_screen_width = 2150  # Width of a single screen (adjust as necessary)
    screen_height = 1080  # Height of the screens

    # Desired video window size
    window_width = 300
    window_height = 300

    # Calculate position to center the window at the bottom of the middle screen
    middle_screen_x_start = single_screen_width  # Start of the middle screen
    window_x = middle_screen_x_start + (single_screen_width - window_width) // 2
    window_y = screen_height - window_height - 50  # Adjust to place it slightly above the bottom edge

    # Video 1 condition
    if 141.5689 < x < 158.4301 and -65 < y < -50 and not video_flags['video1']:
        video_path1 = '/home/omer/Desktop/Autonomous Resope Unit/Avatar_Parent/Avatar video/person_cross.MOV'
        play_video(video_path1, window_x, window_y, window_width, window_height)
        video_flags['video1'] = True
	timestamp = datetime.now().strftime('%H:%M:%S.%f')
	simulation_time = msg.header.seq*0.033333335071821
	Egocar_data = OrderedDict()
	Egocar_data["Type"] = "Face_Status:"
	Egocar_data["Timestamp"] = timestamp
	Egocar_data["Simulation_time"] = simulation_time
	Egocar_data["Video"] = "person_cross"

        write_to_json(Egocar_data) # for json

    # Video 2 condition
    elif 165 < x < 195 and -8 < y < 8 and not video_flags['video2']:
        video_path2 = '/home/omer/Desktop/Autonomous Resope Unit/Avatar_Parent/Avatar video/car_stop.MOV'
        play_video(video_path2, window_x, window_y, window_width, window_height)
        video_flags['video2'] = True

	timestamp = datetime.now().strftime('%H:%M:%S.%f')
	simulation_time = msg.header.seq*0.033333335071821
	Egocar_data = OrderedDict()
	Egocar_data["Type"] = "Face_Status:"
	Egocar_data["Timestamp"] = timestamp
	Egocar_data["Simulation_time"] = simulation_time
	Egocar_data["Video"] = "car_stop"
        write_to_json(Egocar_data) # for json

    # Video 3 condition
    elif 290.00 < x < 310.00  and -7 < y < 7 and not video_flags['video3']:
        video_path3 = '/home/omer/Desktop/Autonomous Resope Unit/Avatar_Parent/Avatar video/person_cross.MOV'
        play_video(video_path3, window_x, window_y, window_width, window_height)
        video_flags['video3'] = True

	timestamp = datetime.now().strftime('%H:%M:%S.%f')
	simulation_time = msg.header.seq*0.033333335071821
	Egocar_data = OrderedDict()
	Egocar_data["Type"] = "Face_Status:"
	Egocar_data["Timestamp"] = timestamp
	Egocar_data["Simulation_time"] = simulation_time
	Egocar_data["Video"] = "person_cross"
        write_to_json(Egocar_data) # for json

    # Video 4 condition
    elif 330.00 < x < 340.00 and -115.00 < y < -95.00 and not video_flags['video4']:
        video_path4 = '/home/omer/Desktop/Autonomous Resope Unit/Avatar_Parent/Avatar video/Avatar video/red_light.MOV'
        play_video(video_path4, window_x, window_y, window_width, window_height)
        video_flags['video4'] = True

	timestamp = datetime.now().strftime('%H:%M:%S.%f')
	simulation_time = msg.header.seq*0.033333335071821
	Egocar_data = OrderedDict()
	Egocar_data["Type"] = "Face_Status:"
	Egocar_data["Timestamp"] = timestamp
	Egocar_data["Simulation_time"] = simulation_time
	Egocar_data["Video"] = "red_light"
        write_to_json(Egocar_data) # for json

    # Video 5 condition
    elif 260.00 < x < 290.00 and -137.00 < y < -123.00 and not video_flags['video5']:
        video_path5 = '/home/omer/Desktop/Autonomous Resope Unit/Avatar_Parent/Avatar video/passing_barrier.MOV'
        play_video(video_path5, window_x, window_y, window_width, window_height)
        video_flags['video5'] = True

	timestamp = datetime.now().strftime('%H:%M:%S.%f')
	simulation_time = msg.header.seq*0.033333335071821
	Egocar_data = OrderedDict()
	Egocar_data["Type"] = "Face_Status:"
	Egocar_data["Timestamp"] = timestamp
	Egocar_data["Simulation_time"] = simulation_time
	Egocar_data["Video"] = "passing_barrier"
        write_to_json(Egocar_data) # for json

# Initialize ROS node
rospy.init_node('Video_Agent')

# Subscribe to the odometry topic
rospy.Subscriber("/carla/ego_vehicle/odometry", Odometry, odometry_callback)

# Set the desired loop frequency (1 Hz in this example)
rate = rospy.Rate(1)

# Continue running the code
while not rospy.is_shutdown():
    rate.sleep()
