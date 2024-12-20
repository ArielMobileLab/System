import carla
import numpy as np
import pygame

# Connect to the CARLA server
client = carla.Client('10.20.0.180', 2000)
client.set_timeout(10.0)

# Get the world object
world = client.get_world()

# Find the ego vehicle (assuming it's named 'ego_vehicle')
ego_vehicle = None
for actor in world.get_actors().filter('vehicle.*'):
    if 'role_name' in actor.attributes and actor.attributes['role_name'] == 'ego_vehicle':
        ego_vehicle = actor
        break

if ego_vehicle is None:
    print("No ego vehicle found")
    exit()

# Find all camera sensors attached to the ego vehicle
cameras = []
for actor in world.get_actors().filter('sensor.camera.rgb'):
    if actor.parent.id == ego_vehicle.id:
        cameras.append(actor)
        para = actor.get_transform()
        print(para)

# Check if any cameras are found
if not cameras:
    print("No cameras found")
    exit()

# Function to check if camera's yaw is less than 100 degrees
def is_yaw_less_than_100(camera):
    transform = camera.get_transform()
    rotation = transform.rotation
    return rotation.yaw > 100

# Select the first camera with yaw less than 100 degrees
selected_camera = None
for camera in cameras:
    if is_yaw_less_than_100(camera):
        selected_camera = camera
        break

if selected_camera is None:
    print("No camera with yaw less than 100 degrees found")
    exit()

print("Selected camera found: {selected_camera.type_id} with yaw: {selected_camera.get_transform().rotation.yaw}")

# Desired resolution of the display for the selected camera
desired_display_width = 1920
desired_display_height = 450

# Render object to keep and pass the Pygame surface
class RenderObject(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))

# Camera sensor callback, reshapes raw data from camera into 2D RGB and applies to Pygame surface
def pygame_callback(data, obj):
    img = np.frombuffer(data.raw_data, dtype=np.uint8).reshape((data.height, data.width, 4))
    img = img[:, :, :3]  # Keep only RGB channels
    img = img[:, :, ::-1]  # Convert BGR to RGB

    # Scale down the image to the desired display resolution
    small_img = pygame.transform.scale(pygame.surfarray.make_surface(img.swapaxes(0, 1)), (obj.width, obj.height))
    obj.surface = small_img

# Initialize Pygame and the display
pygame.init()
display_width = desired_display_width
display_height = desired_display_height
gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('CARLA Camera Feed')

# Create a render object for the selected camera and start the camera with Pygame callback
render_object = RenderObject(desired_display_width, desired_display_height)
selected_camera.listen(lambda image: pygame_callback(image, render_object))

# Game loop
crashed = False
while not crashed:
    # Collect key press events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    # Display the selected camera's feed
    if render_object.surface:
        gameDisplay.blit(render_object.surface, (0, 0))
    
    pygame.display.flip()

# Stop the selected camera and quit Pygame after exiting game loop
selected_camera.stop()
pygame.quit()
