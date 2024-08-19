import pygame
from constants import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import *

print("Starting asteroids!")
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def reset_game(player, asteroids, shots, updateable, drawable):
    """Resets the game state for a replay."""
    Player.containers[0].empty()  # updateable
    Player.containers[1].empty()  # drawable
    Shot.containers[0].empty()    # updateable
    Shot.containers[1].empty()    # shots
    Asteroid.containers[0].empty()  # updateable
    Asteroid.containers[1].empty()  # drawable
    Asteroid.containers[2].empty()  # asteroids

    main()

def main():
    clock = pygame.time.Clock()
    dt = 0.0
    death_time = None
    
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    font2 = pygame.font.Font(None, 180)

    drawable = pygame.sprite.Group()
    updateable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Player.containers = (updateable, drawable)
    Shot.containers = (updateable, shots)
    Asteroid.containers = (updateable, drawable, asteroids)
    AsteroidField.containers = (updateable,)
    
    
    player = Player((SCREEN_WIDTH / 2),(SCREEN_HEIGHT / 2), PLAYER_RADIUS, "player.png")
    asteroid_field = AsteroidField()

    game_over_check = False
    game_over_sound = False

    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if game_over_check and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game(player, asteroids, shots, updateable, drawable)  # Reset the game if "R" is pressed
                return
        screen.fill("black")
        
        for obj in updateable:
            obj.update(dt)
            
        
        for shot in shots:
            shot.draw(screen)
        for obj in drawable:
            obj.draw(screen)
        
        score_text = font.render(f"Score: {player.score}", False, "red")
        score_rect = score_text.get_rect()
        score_rect.topright = (SCREEN_WIDTH - 10, 10)
        screen.blit(score_text, score_rect)
    
        

        if not game_over_check:
            for asteroid in asteroids:
                if player.collision_check(asteroid):
                    print("Game over!")
                    print(player.score)
                    player.kill()
                    ship_death.play()
                    death_time = pygame.time.get_ticks()
                    game_over_check = True
                
                for shot in shots:
                    if asteroid.collision_check(shot):
                        player.score += asteroid.split()
                        shot.kill()
        
        if game_over_check:
            current_time = pygame.time.get_ticks()
            if current_time - death_time > 1100:
                if not game_over_sound:
                    game_over.play()
                    game_over_sound = True
                game_over_msg1 = font2.render("GAME", False, "red")
                x1 = (SCREEN_WIDTH // 2) - (game_over_msg1.get_width() // 2)
                y1 = (SCREEN_HEIGHT // 2) - (game_over_msg1.get_height())
                screen.blit(game_over_msg1, (x1, y1))

                game_over_msg2 = font2.render("OVER!", False, "red")
                x2 = (SCREEN_WIDTH // 2) - (game_over_msg2.get_width() // 2)
                y2 = (SCREEN_HEIGHT // 2)
                screen.blit(game_over_msg2, (x2, y2))

                replay_text = font.render("Press R to Replay", False, "white")
                replay_rect = replay_text.get_rect()
                replay_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130)
                screen.blit(replay_text, replay_rect)


        pygame.display.flip()
        
        dt = (clock.tick(60) / 1000)
        

if __name__ == "__main__":
    main()