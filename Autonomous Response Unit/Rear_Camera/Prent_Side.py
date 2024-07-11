#Code that use the main camera and show in the screen parent side not make another camera

import carla
import numpy as np
import pygame

# Connect to the CARLA server
client = carla.Client('10.20.0.164', 2000)
client.set_timeout(2.0)

# Get the world object
world = client.get_world()

# Find the existing camera sensor
camera = None
for actor in world.get_actors().filter('sensor.camera.rgb'):
    camera = actor
    break

# Check if camera is found
if camera is None:
    print("Camera not found")
    exit()

# Desired resolution of the display
desired_display_width = 1920
desired_display_height = 1080

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

# Start camera with Pygame callback
renderObject = RenderObject(desired_display_width, desired_display_height)
camera.listen(lambda image: pygame_callback(image, renderObject))

# Initialise the Pygame interface
pygame.init()
gameDisplay = pygame.display.set_mode((desired_display_width, desired_display_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('CARLA Camera Feed')

# Game loop
crashed = False

while not crashed:
    # Collect key press events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    if renderObject.surface:
        # Display the scaled-down image directly
        gameDisplay.blit(renderObject.surface, (0, 0))
        pygame.display.flip()




# Stop camera and quit Pygame after exiting game loop
camera.stop()
pygame.quit()

