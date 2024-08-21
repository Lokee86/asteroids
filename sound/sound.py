import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame

pygame.init()
pygame.mixer.init()

laser_sound = pygame.mixer.Sound("sound/laser.wav")
rock_death = pygame.mixer.Sound("sound/explosion.mp3")
rock_death.set_volume(0.5)
ship_death = pygame.mixer.Sound("sound/ship_death.mp3")
game_over = pygame.mixer.Sound("sound/gameover.mp3")