import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load the MP3 file
pygame.mixer.music.load("/home/omer/Desktop/Autonomous Resope Unit/Senario_Voice/road-noise.mp3")

# Play the MP3 file and loop forever
pygame.mixer.music.play(loops=-1, fade_ms=0)

# Keep the program running so the music can play
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
