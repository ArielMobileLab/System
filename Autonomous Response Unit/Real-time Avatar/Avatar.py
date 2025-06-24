import pygame
import pyttsx3
import time
import threading
import random

pygame.init()

# הגדרות חלון
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avatar מדבר")

# צבעים ופונטים
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont("arial", 28)

# טקסט שיוצג
spoken_text = ""
is_speaking = False

# טען תמונות
avatar_img_open = pygame.image.load(r"C:\Users\ALEX\Desktop\Synchronic\Error\Real-time Avatar\smile.PNG")
avatar_img_blink = pygame.image.load(r"C:\Users\ALEX\Desktop\Synchronic\Error\Real-time Avatar\blink.PNG")
mouth_frames = [
    pygame.image.load(r"C:\Users\ALEX\Desktop\Synchronic\Error\Real-time Avatar\mouth1.PNG"),
    pygame.image.load(r"C:\Users\ALEX\Desktop\Synchronic\Error\Real-time Avatar\mouth2.PNG"),
    pygame.image.load(r"C:\Users\ALEX\Desktop\Synchronic\Error\Real-time Avatar\mouth3.PNG"),
]

# מיקום
avatar_pos = (200, 50)

# דיבור
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# מצמוץ
last_blink = pygame.time.get_ticks()
blink_interval = random.randint(4000, 7000)
blinking = False
blink_start = 0
blink_duration = 80

# אנימציית פה
mouth_frame_index = 0
mouth_frame_timer = pygame.time.get_ticks()

# פונקציית דיבור
def speak_text(text):
    global is_speaking, spoken_text
    is_speaking = True
    spoken_text = text
    engine.say(text)
    engine.runAndWait()
    is_speaking = False

# ציור מסך
def draw_screen():
    global blinking, last_blink, blink_interval, blink_start
    global mouth_frame_index, mouth_frame_timer

    screen.fill(WHITE)

    # מצמוץ
    now = pygame.time.get_ticks()
    if not blinking and now - last_blink >= blink_interval:
        blinking = True
        blink_start = now
        avatar_img = avatar_img_blink
    elif blinking and now - blink_start >= blink_duration:
        blinking = False
        last_blink = now
        blink_interval = random.randint(2000, 4000)
        avatar_img = avatar_img_open
    else:
        avatar_img = avatar_img_blink if blinking else avatar_img_open

    screen.blit(avatar_img, avatar_pos)

    # פה משתנה
    if is_speaking:
        if now - mouth_frame_timer > 200:
            mouth_frame_index = (mouth_frame_index + 1) % len(mouth_frames)
            mouth_frame_timer = now
        mouth_img = mouth_frames[mouth_frame_index]
        screen.blit(mouth_img, (avatar_pos[0], avatar_pos[1]))

    # טקסט
    text_surface = font.render(spoken_text, True, BLACK)
    screen.blit(text_surface, (50, HEIGHT - 50))

    pygame.display.flip()

# לולאת pygame
def pygame_loop():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        draw_screen()
        clock.tick(30)

# הפעלת pygame ברקע
threading.Thread(target=pygame_loop, daemon=True).start()

# קלט מהטרמינל
while True:
    user_input = input("מheה אתה רוצה ש-Avatar יגיד? ")
    if user_input.strip():
        speak_text(user_input)
