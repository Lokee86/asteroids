import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame

pygame.init()
pygame.mixer.init()

laser_sound = pygame.mixer.Sound("laser.wav")
rock_death = pygame.mixer.Sound("explosion.mp3")
ship_death = pygame.mixer.Sound("ship_death.mp3")
game_over = pygame.mixer.Sound("gameover.mp3")