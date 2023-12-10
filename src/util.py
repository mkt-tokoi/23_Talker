import pygame


def play_mp3(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def system_prompt():
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()
