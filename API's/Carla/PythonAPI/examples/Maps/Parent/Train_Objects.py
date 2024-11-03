import signal
import os
import psutil

# Signal handler for Ctrl+C
def signal_handler(signal, frame):
    print("\nCtrl+C received. Terminating the process.")
    # Get the process names of all running processes
    process_names = [p.info['name'] for p in psutil.process_iter(attrs=['name'])]
    # Print the process names
    for name in process_names:
        print("Process terminated:", name)
    pid = os.getpid()
    os.kill(pid, signal.SIGINT)

# Set the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Keep the program running until Ctrl+C is pressed
while True:
    pass
