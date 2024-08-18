import pygame
from constants import *
from player import Player

def main():
    print("Starting asteroids!")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0
    
    drawable = pygame.sprite.Group()
    updateable = pygame.sprite.Group()
    Player.containers = (updateable, drawable)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player((SCREEN_WIDTH / 2),(SCREEN_HEIGHT / 2), PLAYER_RADIUS)
    
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        for obj in updateable:
            obj.update(dt)
        
        for obj in drawable:
            obj.draw(screen)
        
        pygame.display.flip()

        dt = (clock.tick(60) / 1000)
        

if __name__ == "__main__":
    main()