import os
import numpy as np
import pandas as pd
from fastdtw import fastdtw
import glob

# Constants
SAMPLE_RATE = 20
MIDWARE_MULTIPLIER = 500
GPS_MULTIPLIER = 512
BASE_PATH = r"H:\My Drive\The Mobile Lab\Lab tasks\Synchroniz\for_Test"

def moving_average(x, n=1500):
    return np.convolve(x, np.ones(n)/n, mode='same')

def tidy_mindware(file_path):
    Mindware = pd.read_csv(file_path)  # Assuming tab-separated
    Mindware.columns = ['Time', 'Bio1', 'Bio2', 'Z0', 'dZ.dt', 'GSC', 'x', 'y', 'z']
    Mindware['SNO'] = np.arange(1, len(Mindware) + 1)
    
    Mindware['x'] -= Mindware['x'].median()
    Mindware['y'] -= Mindware['y'].median()
    Mindware['z'] -= Mindware['z'].median()
    
    Mindware['Acceleration'] = np.sqrt(Mindware['x']**2 + Mindware['y']**2 + Mindware['z']**2)
    Mindware['Acceleration'] = moving_average(Mindware['Acceleration'], 500)
    Mindware['Acceleration'] *= 9.8
    
    Mindware['SNO'] = (Mindware['SNO'] - Mindware['SNO'].mean()) / Mindware['SNO'].std()
    Mindware = Mindware.iloc[::int(MIDWARE_MULTIPLIER / SAMPLE_RATE), :]
    Mindware = Mindware.dropna(subset=['Acceleration'])
    
    return Mindware

def tidy_GPS(file_path):
    GPS = pd.read_excel(file_path)
    GPS['SNO'] = np.arange(1, len(GPS) + 1)
    
    GPS['x'] = GPS['Accel.Linear.X'] - GPS['Accel.Linear.X'].median()
    GPS['y'] = GPS['Accel.Linear.Y'] - GPS['Accel.Linear.Y'].median()
    GPS['z'] = GPS['Accel.Linear.Z'] - GPS['Accel.Linear.Z'].median()
    
    GPS['Acceleration'] = np.sqrt(GPS['x']**2 + GPS['y']**2 + GPS['z']**2)
    GPS['Acceleration'] = moving_average(GPS['Acceleration'], 512)
    
    GPS = GPS.iloc[::int(GPS_MULTIPLIER / SAMPLE_RATE), :]
    GPS = GPS.dropna(subset=['Acceleration'])
    
    return GPS

def sync_data(gps_folder_path, mindware_path, output_path):
        
        #Mindware_matrix
        M = tidy_mindware(mindware_path)
        #GPS_matrix
        G = tidy_GPS(gps_folder_path)

        # DTW between ACC from both Matrixs
        distance, path = fastdtw(G['Acceleration'].values, M['Acceleration'].values)

        #Adding Index
        M['Mindex'] = np.arange(len(M))
        G['Gindex'] = np.arange(len(G))
        
        path = pd.DataFrame(path, columns=["G", "M"])

        # Calculating the Average of G Indexes for Each Index in M
        result = path.groupby('M')['G'].mean().reset_index()

        #re-name coulums
        result.columns = ["Mindex", "Gindex"]

        # merge M with index colum
        M_with_index = pd.merge(M, result, how="left", on="Mindex")

        # merge M with the G matrix
        M_with_index_and_G = pd.merge(M_with_index, G, how="left", on="Gindex")

        # interpolate for missing data due to lane 77 mean prosses
        M_with_index_and_G = M_with_index_and_G.interpolate(method='linear', axis=0)

        # Ensure the folder exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  

        # saving the matrix
        M_with_index_and_G.to_csv(output_path, index=False)
        print(f"✔ Sync completed for {output_path}")


# ---- Main Loop ---- # for finding the Maindware & gps & output path
for participant in os.listdir(BASE_PATH):
    if participant.startswith("C"):  # Check if the folder starts with 'C'
        participant_path = os.path.join(BASE_PATH, participant, "Teleoperation")

        for run_type in ["Close", "Far"]:
                
              #find mindware_path  
              mindware_path = os.path.join(participant_path, "Mindware", run_type, f"{run_type}.txt")

              #out put path
              output_file = os.path.join(participant_path, "Mindware", run_type, f"Sync_Mindware_GPS_{run_type}.csv")

              #find gps path 
              folder_names = [f for f in os.listdir(participant_path) if os.path.isdir(os.path.join(participant_path, f))]

              for folder in folder_names:
                    
                    gps_folder_path = os.path.join(participant_path, folder)
                    
                    # Check if the folder matches the pattern for Accompanied Close or Far
                    if "_Accompanied_Close" in folder and run_type == "Close":
                        print(f"Found Close folder: {gps_folder_path}")
                        sync_data(gps_folder_path,mindware_path,output_file) 
                    elif "_Accompanied_Far" in folder and run_type == "Far":
                        print(f"Found Far folder: {gps_folder_path}")
                        sync_data(gps_folder_path,mindware_path,output_file)    

