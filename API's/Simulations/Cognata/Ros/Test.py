import pandas as pd
import haversine as hs
import numpy as np
import statistics
from datetime import datetime
import matplotlib.pyplot as plt
import itertools

## ---------------------------------------------------------------------------
def filter_acceleration(x):
    high_pass_window=600
    x=x-x.rolling(window=high_pass_window,center=True,min_periods=1).median() ## highpass 
    low_pass_window=10
    x=x.rolling(window=low_pass_window,center=True,min_periods=1).mean()
    x=x-statistics.median(x)
    return x

def Distance_Driven_haversine(Latitude,Longitude,):
    n=len(Latitude)
    Distance_Driven = [0] * n
    for i in np.arange(n-1):
        loc1=(Latitude[i],Longitude[i])
        loc2=(Latitude[i+1],Longitude[i+1])
        Distance_Driven[i+1] = hs.haversine(loc1,loc2,unit='m')
    Distance_Driven = np.cumsum(Distance_Driven)
    return Distance_Driven

#Calculate the distance (in different units) between two points on the earth using their latitude and longitude.
def distanceHaversinePoints(p1_lat,p1_lng,p2_lat,p2_lng):
    loc1=(p1_lat,p1_lng)
    loc2=(p2_lat,p2_lng)
    return hs.haversine(loc1,loc2,unit='m')
    
            
def distanceHaversineVectors(p1_lat,p1_lng,p2_lat,p2_lng):
    distance=[]
    for i in np.arange(len(p1_lat)):
        dis=distanceHaversinePoints(p1_lat[i],p1_lng[i],p2_lat[i],p2_lng[i])
        distance.append(dis)
    return distance

   
def tidy_cognata(path):
    df=pd.read_json(path)
    df = (pd.DataFrame(df['Logs'].values.tolist()).join(df.drop('Logs', 1)))
    df=pd.DataFrame.from_dict(df, orient='columns')
    fixedTime = df.WorldTime[0]
    fixedTime2 = fixedTime[0:15]
    try:
        fixedTime3 = datetime.strptime(fixedTime2, "%H:%M:%S.%f")
    except:
        fixedTime3 = datetime.strptime(fixedTime2+".0", "%H:%M:%S.%f")
    for x in df.index:
        currentTime = df.WorldTime[x]
        currentTime2 = currentTime[0:15]
        try:
            currentTime3 = datetime.strptime(currentTime2, "%H:%M:%S.%f")
        except:
            currentTime3 = datetime.strptime(currentTime2+".0", "%H:%M:%S.%f")
        delta = currentTime3 - fixedTime3
        deltasec = delta.total_seconds()
        df.RealTime[x] = deltasec
    ### Termination
    Termination=df[df.Type=='Termination']
    if len(Termination)>0:
        Termination=Termination[['SimulationTime','Reason']]
    else:
        Termination=pd.DataFrame({
            'SimulationTime':   [max(df['SimulationTime'])], 
            'Reason'        :   ['No termination data']})

    ### Begining
    Begining=pd.DataFrame({
                'SimulationTime':   [min(df['SimulationTime'])], 
                'Reason'        :   ['Start']})
    Termination=Termination.append(Begining)
                
    ### Merge outer join
    df = pd.merge(df, Termination, on='SimulationTime', how='outer')

    return df
         
def tidy_engine(path):
    try:
        #path=r"G:\My Drive\Ariel Uni\A1_012594\Simulator\4.Latency\Latency3\7081(11 20 29)-CognataEngineLog (9).JSON"
        df=pd.read_json(path)
        df = (pd.DataFrame(df['Logs'].values.tolist()).join(df.drop('Logs', 1)))
        df=pd.DataFrame.from_dict(df, orient='columns')
       
### GPS messages
        GPS=df[df.Type=='GPS']
        GPS=GPS.dropna(axis=1, how='all')
        GPS=GPS.drop(['Type'], axis=1)
        GPS["ForwaredAcceleration"]=999.99
        GPS["LateralAcceleration"]=999.99
        GPS["UpwardAcceleration"]=999.99
        for i in np.arange(len(GPS.Acceleration)):     
            GPS["ForwaredAcceleration"].iloc[i]=float(GPS.Acceleration.iloc[i] ['x'])
            GPS["LateralAcceleration"].iloc[i]=float(GPS.Acceleration.iloc[i] ['y'])
            GPS["UpwardAcceleration"].iloc[i]=float(GPS.Acceleration.iloc[i] ['z'])
        
        # The filtered acceleration while later be used to identify kinematic events
        GPS["ForwaredAcceleration"]=filter_acceleration(GPS["ForwaredAcceleration"])
        GPS["LateralAcceleration"]=filter_acceleration(GPS["LateralAcceleration"])
        GPS["UpwardAcceleration"]=filter_acceleration(GPS["UpwardAcceleration"])
        
        GPS=GPS.reset_index()
        GPS["RealTime"] = " "
        GPS["Distance_Driven"]=Distance_Driven_haversine(GPS['Latitude'],GPS['Longitude'])
        
        fixedTime = GPS.WorldTime[0]
        fixedTime2 = fixedTime[0:15]
        try:
            fixedTime3 = datetime.strptime(fixedTime2, "%H:%M:%S.%f")
        except:
            fixedTime3 = datetime.strptime(fixedTime2+".0", "%H:%M:%S.%f")
        for x in GPS.index:
            currentTime = GPS.WorldTime[x]
            currentTime2 = currentTime[0:15]
            try:
                currentTime3 = datetime.strptime(currentTime2, "%H:%M:%S.%f")
            except:
                currentTime3 = datetime.strptime(currentTime2+".0", "%H:%M:%S.%f")
            delta = currentTime3 - fixedTime3
            deltasec = delta.total_seconds()
            GPS.RealTime[x] = deltasec
            
        GPS['CumulativeSpeed']=np.cumsum(GPS.Speed)
        GPS['CumulativeSpeedPWR2']=np.cumsum(GPS.Speed**2)
        GPS['Samples']=np.arange(len(GPS))+1

### CarTelemetries messages
        CarTelemetries=df[df.Type=='CarTelemetries']
        CarTelemetries=CarTelemetries.dropna(axis=1, how='all')
        CarTelemetries.Acceleration=pd.to_numeric(CarTelemetries.Acceleration)
        CarTelemetries["Longitudinal_Acceleration"]=pd.to_numeric(CarTelemetries.Acceleration)
        CarTelemetries=CarTelemetries.drop(['Type', 'WorldTime', 'FrameID', 'Speed','Acceleration'], axis=1)
        df_wide = pd.merge(GPS, CarTelemetries, on='SimulationTime', how='outer')
### Termination
        Termination=df[df.Type=='Termination']
        if len(Termination)>0:
             Termination=Termination[['SimulationTime','Reason']]
            #Termination=Termination.drop(['Type', 'WorldTime', 'FrameID','Speed','Distance_Driven'], axis=1)
        else:
            Termination=pd.DataFrame({
                    'SimulationTime':   [max(GPS['SimulationTime'])], 
                    'Reason'        :   ['No termination data']})

### Begining
        Begining=pd.DataFrame({
            'SimulationTime':   [min(GPS['SimulationTime'])], 
            'Reason'        :   ['Start']})
        Termination=Termination.append(Begining)
        

### Merge outer join
        df_wide = pd.merge(df_wide, Termination, on='SimulationTime', how='outer')
        df_wide = df_wide[df_wide['FrameID'].isna()==False]
    except:
        return None
    return df_wide

def tidy_gps(path):  # load json to gsp df
    try:
        df = pd.read_json(path)   
        df = pd.DataFrame(df['Logs'].values.tolist()).join(df.drop('Logs', 1))
        df = pd.DataFrame.from_dict(df, orient='columns')
        df = df[df['Name'].isin(['Lead Vehicle', 'lead car','carinfront'])].reset_index()     
        
        df["ForwaredAcceleration"]=999.99
        df["LateralAcceleration"]=999.99
        df["UpwardAcceleration"]=999.99
        for i in np.arange(len(df.Acceleration)):     
           df["ForwaredAcceleration"].iloc[i]=float(df.Acceleration.iloc[i] ['x'])
           df["LateralAcceleration"].iloc[i]=float(df.Acceleration.iloc[i] ['y'])
           df["UpwardAcceleration"].iloc[i]=float(df.Acceleration.iloc[i] ['z'])
       
       # The filtered acceleration while later be used to identify kinematic events
        df["ForwaredAcceleration"]=filter_acceleration(df["ForwaredAcceleration"])
        df["LateralAcceleration"]=filter_acceleration(df["LateralAcceleration"])
        df["UpwardAcceleration"]=filter_acceleration(df["UpwardAcceleration"])
       
        df=df.reset_index()
        df["RealTime"] = " "
        df["Distance_Driven"]=Distance_Driven_haversine(df['Latitude'],df['Longitude'])
        fixedTime = df.WorldTime[0]
        fixedTime2 = fixedTime[0:15]
        fixedTime3 = datetime.strptime(fixedTime2, "%H:%M:%S.%f")
        for x in df.index:
            currentTime = df.WorldTime[x]
            currentTime2 = currentTime[0:15]
            currentTime3 = datetime.strptime(currentTime2, "%H:%M:%S.%f")

            delta = currentTime3 - fixedTime3
            deltasec = delta.total_seconds()
            df.RealTime[x] = deltasec
            
        df = df[['SimulationTime', 'Latitude', 'Longitude','RealTime','WorldTime','Speed','ForwaredAcceleration','LateralAcceleration','Name']] 
        
        ### Termination
        Termination=pd.DataFrame({
            'SimulationTime':   [max(df['SimulationTime'])], 
            'Reason'        :   ['No termination data']})

### Begining
        Begining=pd.DataFrame({
            'SimulationTime':   [min(df['SimulationTime'])], 
            'Reason'        :   ['Start Simulation']})
        Termination=Termination.append(Begining)

### miscellaneous 
        df['Distance_Driven']=None    ## currently we don't need the Distance_Driven the columns is added for
        df['CumulativeSpeed']=None    ## currently we don't need the Distance_Driven the columns is added for
        df['Samples']=None    ## currently we don't need the Distance_Driven the columns is added for
        df['CumulativeSpeedPWR2']=None    ## currently we don't need the Distance_Driven the columns is added for
        df['CumulativeDistanceToLead']=None    ## currently we don't need the Distance_Driven the columns is added for
        df['CumulativeDistanceToLeadPWR2']=None 
        df = pd.merge(df, Termination, on='SimulationTime', how='outer')

    except:
        return None
    return df

def tidy_teleoperation(path):
    df = pd.read_excel(path)
    if (len(df)>0):
        df=df.rename(columns = {'measurement time':'measurement_time'})
        df=df.rename(columns = {'Pose.Position.X':'Latitude'})
        df=df.rename(columns = {'Pose.Position.Y':'Longitude'})
        df=df.rename(columns = {'Pose.Orientation.X':'Pose_Orientation_X'})
        df=df.rename(columns = {'Pose.Orientation.Y':'Pose_Orientation_Y'})
        df=df.rename(columns = {'Velocity.Linear.X':'Speed'})
        df=df.rename(columns = {'Velocity.Linear.Y':'Velocity_Linear_Y'})
        df=df.rename(columns = {'Accel.Linear.X':'ForwaredAcceleration'})
        df=df.rename(columns = {'Accel.Linear.Y':'LateralAcceleration'})
        df=df.rename(columns = {'Accel.Linear.Z':'UpwardAcceleration'})
        
        # The filtered acceleration while later be used to identify kinematic events
        df["ForwaredAcceleration"]=df["ForwaredAcceleration"].rolling(128,center=True,min_periods=1).mean()
        df["LateralAcceleration"]=df["LateralAcceleration"].rolling(128,center=True,min_periods=1).mean()
        df["UpwardAcceleration"]=df["UpwardAcceleration"].rolling(128,center=True,min_periods=1).mean()
        
        Distance_Driven = (np.diff(df.Latitude)**2 + np.diff(df.Longitude)**2)**0.5
        Distance_Driven = np.pad(Distance_Driven, (1, 0), 'constant', constant_values=(0))
        Distance_Driven = np.cumsum(Distance_Driven)
        df['Distance_Driven']=Distance_Driven ## It is the same name as in the simulator files
        df['CumulativeSpeed']=np.cumsum(df.Speed)
        df['CumulativeSpeedPWR2']=np.cumsum(df.Speed**2)
        df['Samples']=np.arange(len(df))+1
        df['SimulationTime']= df['measurement_time'] ##For allignment with cognata files
        df['RealTime']= df['measurement_time'] ##For allignment with cognata files
        ##For allignment with cognata files
        df_time = pd.DataFrame({
            'year': list(itertools.repeat(2021, len(df))),
            'month':list(itertools.repeat(1, len(df))),
            'day': list(itertools.repeat(1, len(df))),
            'hour': df['Time-H'],
            'minute': df['Time-M'],
            'second': np.floor(df['Time-S']),
            'ms': (df['Time-S']-np.floor(df['Time-S']))*1000})

        df['WorldTime']= pd.to_datetime(df_time)
        

                ### Termination
        Termination=pd.DataFrame({
            'SimulationTime':   [max(df['SimulationTime'])], 
            'Reason'        :   ['No termination data']})

### Begining
        Begining=pd.DataFrame({
            'SimulationTime':   [min(df['SimulationTime'])], 
            'Reason'        :   ['Start Simulation']})
        Termination=Termination.append(Begining)
### miscellaneous 
        df['CumulativeDistanceToLead']=None    ## currently we don't need the Distance_Driven the columns is added for
        df['CumulativeDistanceToLeadPWR2']=None 
        df = pd.merge(df, Termination, on='SimulationTime', how='outer')

    return df

# =============================================================================
# Internals
# =============================================================================
def signal_zerocrossings(signal, direction="both"):
    df = np.diff(np.sign(signal))
    if direction in ["positive", "up"]:
        zerocrossings = np.where(df > 0)[0]
    elif direction in ["negative", "down"]:
        zerocrossings = np.where(df < 0)[0]
    else:
        zerocrossings = np.nonzero(np.abs(df) > 0)[0]

    return zerocrossings

def findpeaks(x,thresh=0.2):
    peaks_list = []
    onsets_list = []
    ends_list= []
    amps_list = []
    
    # zero crossings
    pos_crossings = signal_zerocrossings(x-thresh, direction="positive")
    neg_crossings = signal_zerocrossings(x-thresh, direction="negative")
    if len(pos_crossings)>0 and len(neg_crossings)>0:
        neg_crossings = neg_crossings[neg_crossings>min(pos_crossings)]
    # Sanitize consecutive crossings
        if len(pos_crossings) > len(neg_crossings):
            pos_crossings = pos_crossings[0:len(neg_crossings)]
        elif len(pos_crossings) < len(neg_crossings):
            neg_crossings = neg_crossings[0:len(pos_crossings)]

        for i, j in zip(pos_crossings, neg_crossings):
            if j>i:
                window = x[i:j]
                amp = np.max(window)
                peak = np.arange(i,j)[window == amp][0]
                peaks_list.append(peak)
                onsets_list.append(i)
                amps_list.append(amp)
                ends_list.append(j)
            
    # output
        info = {"Onsets": np.array(onsets_list),
                "Peaks": np.array(peaks_list),
                "Amplitude": np.array(amps_list),
                "Ends": np.array(ends_list)}
        return info
    return None

### find the simulation time most near to a point
## The data must have the columns: lng & lat
def distance_to_point(data,point_lat,point_lng, dist_function="haversine"):
    if dist_function=="haversine":
        loc1=(point_lat,point_lng)
        loc2=(data['lat'],data['lng']) 
        rep=hs.haversine(loc1,loc2,unit='m')
    else:
        rep=((data['lng']-point_lng)**2+(data['lat']-point_lat)**2)**0.5
    return rep

def find_the_time_most_reasnable_for_point(lat,lng,time,point_lat,point_lng,distance_function="haversine"): 
    df = pd.DataFrame({'lat': lat,'lng': lng,'time': time}) 
    epsilon=0.00005
    v=(df.lat>point_lat-epsilon) & (df.lat<point_lat+epsilon) & (df.lng>point_lng-epsilon) & (df.lng<point_lng+epsilon)
    if np.sum(v)==0:
        return None
    df=df[v]
    if (df.time.max()-df.time.min())>30: ## more than 30 seconds in the event is not reasnable when driving.
        return None
    df.insert(0,'distance',df.apply(distance_to_point,args=(point_lat,point_lng,distance_function),axis=1))
    estimated_time=np.average(df.time, weights=1/pow(df.distance,4))
    return estimated_time

def find_the_time_most_reasnable_for_point_v2(lat,lng,time,point_lat,point_lng,event_number=1,distance_function="euclidean"): 
    
    # lat=df_wide.Latitude
    # lng=df_wide.Longitude
    # time=df_wide.SimulationTime
    # point_lat=subset.Latitude[index]
    # point_lng=subset.Longitude[index]
    # event_number=subset.Arrivel_Number[index]
    # distance_function=subset.Distance_Function[index]
    
    estimated_time=None
    columns = ["lat", "lng", "time"]
    a=np.array([lat,lng,time]) 
    a=a.transpose()
    df = pd.DataFrame(a,columns=columns) 
    df.insert(0,'distance',df.apply(distance_to_point,args=(point_lat,point_lng,distance_function),axis=1))
    picks=findpeaks(1/df.distance,thresh=1/5.5) ##1/devided by threshoold distance so short distance will translate to a large number
    picks=pd.DataFrame(picks)
    if len(picks)>=event_number:
        picks=picks.loc[event_number-1]
        df_event=df.loc[picks["Onsets"]:picks["Ends"]]
        estimated_time=np.average(df_event.time, weights=1/pow(df_event.distance,4))
    return estimated_time