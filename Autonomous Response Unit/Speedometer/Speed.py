
import os
import signal
import subprocess
speed_process_id = None

def run_speedometer():
        
        global speed_process_id
        # os.system(
        #    'terminator --geometry=340x130-2700+1000 -T speed -p speed -x rosrun cognata_sdk #speed.py')  # Will die when run thread dies (daemon)
        cmd = ["rosrun", "cognata_sdk", "speed_carla.py"]
		
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=set_death_signal(), )
        #save the process id of the speed
        speed_process_id = proc.pid 
        print("hi")
    # END OF LAUNCHSCENARIO CLASS

#close the speed when death signal is send
def set_death_signal():
    def _set_death_signal():
        os.prctl(os.PR_SET_PDEATHSIG, signal.SIGTERM)



# Define a function to send a termination signal to the speed process
def terminate_speed_process(process_id):
    try:
        # Send a SIGTERM signal to the process
        os.kill(process_id, signal.SIGTERM)
    except ProcessLookupError:
        pass  # Process may have already exited

run_speedometer()
