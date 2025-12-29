import socket
import time
import ast  # Safe parsing of string to tuple
import math
import numpy as np
import pandas as pd




Final_value_Array = []
Face_State = 2



UDP_IP = "127.0.0.1"
UDP_PORT = 5005
UDO_IP_OUT = "10.20.0.184"
UDP_PORT_OUT = 12357

send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))



def send_udp_message_to_avatar_generatore(Stress_Model):
        print(Stress_Model)


        global Face_State

        if Face_State == 2:
            #if Stress_Model > 1.26:	 #face 3
            if Stress_Model > 1.3:	 #face 3
                Face_State = 3
                voice_data = (
                             "en-US-DavisNeural",  # Voice name
                             "terrified",            # Category
                             "1",                  # Styledegree
                             "+0%",                  # Pitch
                             "medium",                  # Rate
                             "loud",                  # Volume
                             "watch out!!")  # Text
                message = str(voice_data).encode('utf-8')
                send_sock.sendto(message, (UDO_IP_OUT, UDP_PORT_OUT))
                print(message)


                


        # elif Face_State == 1:
        #     if Stress_Model > 0.8:  #face 2
        #         Face_State = 2
                
        #         voice_data = (
        #                      "en-US-DavisNeural",  # Voice name
        #                      "happy",            # Category
        #                      "1",                  # Styledegree
        #                      "+0%",                  # Pitch
        #                      "medium",                  # Rate
        #                      "loud",                  # Volume
        #                      "I will get my belt on")  # Text
        #         message = str(voice_data).encode('utf-8')
        #         send_sock.sendto(message, (UDO_IP_OUT, UDP_PORT_OUT))
        #         print(message)
                


        elif Face_State == 3:
            if Stress_Model < 1.10: #face 2 
                Face_State = 2
                voice_data = (
                             "en-US-DavisNeural",  # Voice name
                             "terrified",            # Category
                             "1",                  # Styledegree
                             "+0%",                  # Pitch
                             "medium",                  # Rate
                             "loud",                  # Volume
                             "pay attention please")  # Text
                message = str(voice_data).encode('utf-8')
                #send_sock.sendto(message, (UDO_IP_OUT, UDP_PORT_OUT))
                print(message)



def process_udp_message_from_Preception(message):

    global Final_value_Array

    # Split the message by '|' and strip whitespace
    parts = [part.strip() for part in message.split('|')]

    # Check if the message is from Challenge1
    if not parts or not parts[0].startswith("Challenge1"):
        # Ignore messages not from Challenge1
        return

    # Initialize variables for acceleration components
    lin_acc_x = None
    lin_acc_y = None
    lin_acc_z = None

    # Loop through parts to find acceleration components
    for part in parts:
        if part.startswith('acceleration.x:'):
            try:
                lin_acc_x = float(part.split(':')[1].strip())
            except Exception as e:
                print("Failed to parse acceleration.x:", e)

        elif part.startswith('acceleration.y:'):
            try:
                lin_acc_y = float(part.split(':')[1].strip())
            except Exception as e:
                print("Failed to parse acceleration.y:", e)


    Final_value = math.sqrt(lin_acc_x**2 + lin_acc_y**2)
    Final_value_Array.append(Final_value)
    Final_value_Array[:] = Final_value_Array[-20:]  # Keep only the last 20 elements
    Final_value_series = pd.Series(Final_value_Array)
    # Apply rolling median to the Series
    window_size = 5
    median_filtered_array = Final_value_series.rolling(window=window_size).median()
    Acceleration_Mean = np.nanmean(median_filtered_array)
    Stress_Model = 1.052638638*Acceleration_Mean**0.142

    send_udp_message_to_avatar_generatore(Stress_Model)
    

def main():
    
    print(f"UDP server listening on {UDP_IP}:{UDP_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size 1024 bytes
        message = data.decode('utf-8')
        #print(f"Received message from {addr}: {message}")
        process_udp_message_from_Preception(message)

if __name__ == "__main__":
    main()
