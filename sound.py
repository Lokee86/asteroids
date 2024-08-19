import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame

pygame.init()
pygame.mixer.init()

laser_sound = pygame.mixer.Sound("laser.wav")
rock_death = pygame.mixer.Sound("explosion.mp3")