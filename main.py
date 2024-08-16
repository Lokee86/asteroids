import pygame
from constants import *

def main():
    print("Starting asteroids!")
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        window.fill((0, 0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    main()