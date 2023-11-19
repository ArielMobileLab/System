import carla
import random
import logging
import glob
import os
import sys
import time
import weakref
import rospy
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry


#Code that Generate walker that cross the road by Condition from the location of the Ego car



# Add CARLA Python API to the system path
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


#Connect To carla Server as Client
client = carla.Client('localhost', 2000)
#Retrieve the CARLA world
world = client.get_world() 
# Set up the simulator in synchronous mode
settings = world.get_settings()
settings.synchronous_mode = True
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

# Lists to store vehicles, walkers, and actor IDs
walkers = []
all_id = []
all_actors = []

first_walker_cross = True
secound_walker_cross = True

def first_walker_cross1():
		
        global all_id
        global walkers
        global all_actors

    # try:

        # -------------
        # Spawn Walker
        # -------------
        # Define settings for pedestrians
        percentagePedestriansRunning =  0   # Percentage of pedestrians running
        percentagePedestriansCrossing = 2   # Percentage of pedestrians crossing roads
        number_of_walkers = 2

        # Select walker blueprints
        blueprintsWalkers = select_walker_blueprints(world, 'walker.pedestrian.*')
        SpawnActor = carla.command.SpawnActor

        # 1. Find suitable random locations to spawn walkers
        spawn_points = []
        
        for i in range(number_of_walkers):

            #spawn_point = carla.Transform()
            #loc = world.get_random_location_from_navigation()

                # two walkers to cross the road example
                #Walkerlocation1 = carla.Location(x=34.907337, y=-14.626545, z=0.300000) -->train
                
            Walkerlocation1 = carla.Location(x=92.174629, y=45.078133, z=0.300000)
                #Walkerlocation2 = carla.Location(x=342, y=45.2, z=0.300000) 

                # Create walker spawn points using the defined locations
            spawn_points = [carla.Transform(Walkerlocation1)]

         

            # elif (loc != None):
            #     spawn_point.location = loc
            #     spawn_points.append(spawn_point)
                
        
        # 2. Spawn walker objects
        batch = []
        walker_speed = []
        for spawn_point in spawn_points:  # Use walker spawn points
            walker_bp = random.choice(blueprintsWalkers)

            # Set walker attributes
            if walker_bp.has_attribute('is_invincible'):
                walker_bp.set_attribute('is_invincible', 'false')

            # Set walker speed
            if walker_bp.has_attribute('speed'):
                if random.random() > percentagePedestriansRunning:
                    # Walking
                    walker_speed.append(walker_bp.get_attribute('speed').recommended_values[1])
                else:
                    # Running
                    walker_speed.append(walker_bp.get_attribute('speed').recommended_values[2])
            else:
                print("Walker has no speed")
                walker_speed.append(0.0)

            batch.append(SpawnActor(walker_bp, spawn_point))

        results = client.apply_batch_sync(batch, True)
        
        walker_speed2 = []
        for i in range(len(results)):
            if results[i].error:
                logging.error(results[i].error)
            else:
                walkers.append({"id": results[i].actor_id})
                walker_speed2.append(walker_speed[i])
        walker_speed = walker_speed2

        # 3. Spawn walker controllers
        batch = []
        walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
        for i in range(len(walkers)):
            batch.append(SpawnActor(walker_controller_bp, carla.Transform(), walkers[i]["id"]))

        results = client.apply_batch_sync(batch, True)
        for i in range(len(results)):
            if results[i].error:
                logging.error(results[i].error)
            else:
                walkers[i]["con"] = results[i].actor_id

        # 4. Combine walker and controller IDs to get the objects
        for i in range(len(walkers)):
            all_id.append(walkers[i]["con"])
            all_id.append(walkers[i]["id"])

        all_actors = world.get_actors(all_id)

        # 5. Initialize each controller and set targets for walking
        # (list is [controller, actor, controller, actor ...])
        # Set how many pedestrians can cross the road
        world.set_pedestrians_cross_factor(percentagePedestriansCrossing)
        
        for i in range(0, len(all_id), 2):
            
            # Start walker
            all_actors[i].start()
            # Set the target location to walk to a random point
            all_actors[i].go_to_location(world.get_random_location_from_navigation())
            # Set maximum walking speed
            all_actors[i].set_max_speed(float(walker_speed[int(i/2)]))

        print('Spawned %d walkers, press Ctrl+C to exit.' % len(walkers))
  
                
        locp = carla.Location(x=104.868797, y=59.990105, z=0.300000) #person target location 
                
        all_actors[0].go_to_location(locp) # tell the walker to cross the road 

                 
def secound_walker_cross2():
        global all_id
        global walkers
        print("walker_2")
    # try:

        # -------------
        # Spawn Walker
        # -------------
        # Define settings for pedestrians
        percentagePedestriansRunning =  0   # Percentage of pedestrians running
        percentagePedestriansCrossing = 2   # Percentage of pedestrians crossing roads
        number_of_walkers = 2

        # Select walker blueprints
        blueprintsWalkers = select_walker_blueprints(world, 'walker.pedestrian.*')
        SpawnActor = carla.command.SpawnActor

        # 1. Find suitable random locations to spawn walkers
        spawn_points = []
        
        for i in range(number_of_walkers):

            #spawn_point = carla.Transform()
            #loc = world.get_random_location_from_navigation()

           
                # two walkers to cross the road example
                #Walkerlocation1 = carla.Location(x=34.907337, y=-14.626545, z=0.300000) -->train
                
                Walkerlocation1 = carla.Location(x=86.137009, y=78.935600, z=0.300000)
                 

                # Create walker spawn points using the defined locations
                spawn_points = [carla.Transform(Walkerlocation1)]

                

            # elif (loc != None):
            #     spawn_point.location = loc
            #     spawn_points.append(spawn_point)
                
        
        # 2. Spawn walker objects
        batch = []
        walker_speed = []
        for spawn_point in spawn_points:  # Use walker spawn points
            walker_bp = random.choice(blueprintsWalkers)

            # Set walker attributes
            if walker_bp.has_attribute('is_invincible'):
                walker_bp.set_attribute('is_invincible', 'false')

            # Set walker speed
            if walker_bp.has_attribute('speed'):
                if random.random() > percentagePedestriansRunning:
                    # Walking
                    walker_speed.append(walker_bp.get_attribute('speed').recommended_values[1])
                else:
                    # Running
                    walker_speed.append(walker_bp.get_attribute('speed').recommended_values[2])
            else:
                print("Walker has no speed")
                walker_speed.append(0.0)

            batch.append(SpawnActor(walker_bp, spawn_point))

        results = client.apply_batch_sync(batch, True)
        
        walker_speed2 = []
        for i in range(len(results)):
            if results[i].error:
                logging.error(results[i].error)
            else:
                walkers.append({"id": results[i].actor_id})
                walker_speed2.append(walker_speed[i])
        walker_speed = walker_speed2

        # 3. Spawn walker controllers
        batch = []
        walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
        for i in range(len(walkers)):
            batch.append(SpawnActor(walker_controller_bp, carla.Transform(), walkers[i]["id"]))

        results = client.apply_batch_sync(batch, True)
        for i in range(len(results)):
            if results[i].error:
                logging.error(results[i].error)
            else:
                walkers[i]["con"] = results[i].actor_id

        # 4. Combine walker and controller IDs to get the objects
        for i in range(len(walkers)):
            all_id.append(walkers[i]["con"])
            all_id.append(walkers[i]["id"])

        all_actors = world.get_actors(all_id)

	# For control the trafic lights~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        actors = world.get_actors()

        # 5. Initialize each controller and set targets for walking
        # (list is [controller, actor, controller, actor ...])
        # Set how many pedestrians can cross the road
        world.set_pedestrians_cross_factor(percentagePedestriansCrossing)
        
        for i in range(0, len(all_id), 2):
            
            # Start walker
            all_actors[i].start()
            # Set the target location to walk to a random point
            all_actors[i].go_to_location(world.get_random_location_from_navigation())
            # Set maximum walking speed
            all_actors[i].set_max_speed(float(walker_speed[int(i/2)]))

        print('Spawned %d walkers, press Ctrl+C to exit.' % len(walkers))
  
     
        locp = carla.Location(x=104.868797, y=59.990105, z=0.300000) #person target location 
                
        all_actors[0].go_to_location(locp) # tell the walker to cross the road 
                 
      
    # finally:
    #     cleanup(world, walkers, client) # clean the world


# Function to select walker blueprints
def select_walker_blueprints(world, filter):
    bps = world.get_blueprint_library().filter(filter)
    return bps


# Function to clean up and end the simulation
def cleanup(world, vehicles, client):
    all_actors = world.get_actors(all_id)
    settings = world.get_settings()
    settings.synchronous_mode = False
    settings.no_rendering_mode = False
    settings.fixed_delta_seconds = None
    world.apply_settings(settings)

    # Stop walker controllers (list is [controller, actor, controller, actor ...])
    for i in range(0, len(all_id), 2):
        all_actors[i].stop()
        
    client.apply_batch([carla.command.DestroyActor(x) for x in all_id])


def Cross_Walker(data):

    world.tick()
    
    global first_walker_cross
    global secound_walker_cross

   
    # if first_walker_cross == True :
    #   first_walker_cross1()
    #   first_walker_cross = False

    if secound_walker_cross == True and 115.0<data.pose.pose.position.x<116.722782898 and -130.0<data.pose.pose.position.y<-129.0 :
        print("walker_2")
        secound_walker_cross2()
        secound_walker_cross = False
    

if __name__ == '__main__':
        

        rospy.init_node('message_listener1')
        
        # Subscribe to the topic that publishes the messages
        rospy.Subscriber('/carla/ego_vehicle/odometry',Odometry, Cross_Walker, queue_size=1)  

        # Set the desired loop frequency (1 Hz)
        rate = rospy.Rate(1)

        # Continue running the code
        while not rospy.is_shutdown():

        # Sleep to maintain the desired loop frequency
           rate.sleep()
