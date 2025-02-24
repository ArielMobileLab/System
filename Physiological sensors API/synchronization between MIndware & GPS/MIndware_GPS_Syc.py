import pandas as pd

# File paths (Update these with your actual file names)
main_file = r"C:\Users\ALEX\Desktop\Synchronic\test\4/M_with_Aligned_GPS_Time.xlsx"     # Your main file
lookup_file = r"C:\Users\ALEX\Desktop\Synchronic\test\4/processed_gps.xlsx"  # Your lookup file

# Load the Excel files
df_main = pd.read_excel(main_file)
df_lookup = pd.read_excel(lookup_file)

# Ensure column names match
print("Main file columns:", df_main.columns)
print("Lookup file columns:", df_lookup.columns)
# Merge using the correct column names
df_main = df_main.merge(df_lookup[['GPS.Time', 'Acceleration']], 
                        left_on='Aligned_GPS_Time', 
                        right_on='GPS.Time', 
                        how='left')

# Drop the extra 'GPS.Time' column after merging
df_main.drop(columns=['GPS.Time'], inplace=True)

# Rename 'Acceleration' to 'Acceleration gps'
df_main.rename(columns={'Acceleration': 'Acceleration gps'}, inplace=True)

# Save the updated main file
updated_file = r"C:\Users\ALEX\Desktop\Synchronic\test\4/updated_file.xlsx"     # Your main file
df_main.to_excel(updated_file, index=False)

print(f"Updated file saved as '{updated_file}'")



import numpy as np
import pandas as pd
from fastdtw import fastdtw
from collections import defaultdict
from scipy.interpolate import interp1d

sample_rate = 20
midware_multiplayer =500
gps_multiplayer = 512


def moving_average(x, n=1500):
    return np.convolve(x, np.ones(n)/n, mode='same')

def tidy_mindware():

    file_name = r"C:\Users\ALEX\Desktop\Synchronic/Mind.xlsx"
    Mindware = pd.read_excel(file_name)
    print(Mindware.shape)

    Mindware.columns = ['Time', 'Bio1', 'Bio2', 'Z0', 'dZ.dt', 'GSC', 'x', 'y', 'z']
    Mindware['SNO'] = np.arange(1, len(Mindware) + 1) 
    
    Mindware['x'] -= Mindware['x'].median()
    Mindware['y'] -= Mindware['y'].median()
    Mindware['z'] -= Mindware['z'].median()
    
    Mindware['Acceleration'] = np.sqrt(Mindware['x']**2 + Mindware['y']**2 + Mindware['z']**2) 
    Mindware['Acceleration'] = moving_average(Mindware['Acceleration'], 500) 
    Mindware['Acceleration'] *= 9.8 # fix Acc 9.8
    
    Mindware['SNO'] = (Mindware['SNO'] - Mindware['SNO'].mean()) / Mindware['SNO'].std()
    Mindware = Mindware.iloc[::int(midware_multiplayer/sample_rate), :]  
    Mindware = Mindware.dropna(subset=['Acceleration'])
    print("Done mind")    
    print(Mindware.shape)

    return Mindware

#Mindware_matrix
M = tidy_mindware()

def tidy_GPS():
    file_path = r"C:\Users\ALEX\Desktop\Synchronic/gps.xlsx"
    GPS = pd.read_excel(file_path)
    GPS['SNO'] = np.arange(1, len(GPS) + 1) 
    print(GPS.shape)

    GPS['x'] = GPS['Accel.Linear.X'] - GPS['Accel.Linear.X'].median()
    GPS['y'] = GPS['Accel.Linear.Y'] - GPS['Accel.Linear.Y'].median()
    GPS['z'] = GPS['Accel.Linear.Z'] - GPS['Accel.Linear.Z'].median()
    
    GPS['Acceleration'] = np.sqrt(GPS['x']**2 + GPS['y']**2 + GPS['z']**2)
    GPS['Acceleration'] = moving_average(GPS['Acceleration'], 512)
    
    GPS = GPS.iloc[::int(gps_multiplayer/sample_rate), :] 
    GPS = GPS.dropna(subset=['Acceleration'])
    print("done gps")
    print(GPS.shape)
    GPS.to_excel(r"C:\Users\ALEX\Desktop\Synchronic\processed_gps.xlsx", index=False)
    return GPS

#GPS_matrix
G = tidy_GPS()

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

# saving the matrix
output_file_csv = r"C:\Users\ALEX\Desktop\Synchronic\Scy_GPS_Mindware.csv"
M_with_index_and_G.to_csv(output_file_csv, index=False)
