import pygame
from constants import *
print("Starting asteroids!")
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load("graphics/background.png").convert_alpha()
from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import *

# Load animations
player_explosion_frames = []
for i in range(0, 11):
    image = pygame.image.load(f"graphics/Explo__00{i}.png").convert_alpha()
    image = pygame.transform.scale(image, (3.5 * PLAYER_RADIUS, 3.5 * PLAYER_RADIUS))
    player_explosion_frames.append(image)
shot_explosion_frames = []
for i in range(1, 7):
    image = pygame.image.load(f"graphics/OrangeBulletExplo ({i}).png").convert_alpha()
    image = pygame.transform.scale(image, (2 * SHOT_RADIUS, 2 * SHOT_RADIUS))
    shot_explosion_frames.append(image)

def pause_game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                return

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
    
    
    player = Player((SCREEN_WIDTH / 2),(SCREEN_HEIGHT / 2), PLAYER_RADIUS, "graphics/player.png")
    asteroid_field = AsteroidField()

    game_over_check = False
    game_over_sound = False
    player_explosion_active = False
    explosion_index = 0
    explosion_start_time = None
    shot_explosions = []


    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    keys = pygame.key.get_pressed()
    while True:
        if keys[pygame.K_p]:
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press 'P' to initiate pause
                    pause_game()

            if game_over_check and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game(player, asteroids, shots, updateable, drawable)  # Reset the game if "R" is pressed
                return
        
        screen.fill("black")
        for x in range(0, SCREEN_WIDTH, background.get_size()[0]):
            for y in range(0, SCREEN_HEIGHT, background.get_size()[1]):
                screen.blit(background, (x, y))

        
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
    
        
        # Collision checks
        if not game_over_check:
            for asteroid in asteroids:
                if player.collision_check(asteroid):
                    offset = (asteroid.rect.left - player.rect.left, asteroid.rect.top - player.rect.top)
                    if player.mask.overlap(asteroid.mask, offset):
                        print("Game over!")
                        print(player.score)
                        ship_death.play()
                        death_time = pygame.time.get_ticks()
                        player_explosion_active = True
                        explosion_start_time = pygame.time.get_ticks()
                        game_over_check = True
                        player.kill()

                for shot in shots:
                    if asteroid.collision_check(shot):
                        offset = (asteroid.rect.left - shot.rect.left, asteroid.rect.top - shot.rect.top)
                        if shot.mask.overlap(asteroid.mask, offset):
                            player.score += asteroid.split()
                            shot.kill()
                            shot_explosions.append({"position": shot.rect.center, "start_time": pygame.time.get_ticks(), "active": True})
                    
        if player_explosion_active:
            current_time = pygame.time.get_ticks()
            
            # Calculate the time passed since the explosion started
            elapsed_time = current_time - explosion_start_time
            
            # Assume each frame should be shown for 100 milliseconds
            explosion_index = elapsed_time // FRAME_DURATION
            
            if explosion_index < len(player_explosion_frames):
                # Display the current explosion frame
                explosion_frame = player_explosion_frames[explosion_index]
                explosion_rect = explosion_frame.get_rect(center=player.rect.center)
                screen.blit(explosion_frame, explosion_rect.topleft)  # Position it where the player was
            else:
                # Explosion animation is done
                player_explosion_active = False
                # Continue with the game over logic

        for explosion in shot_explosions:
            if explosion["active"]:
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - explosion["start_time"]
                explosion_index = elapsed_time // (FRAME_DURATION // 2)

                if explosion_index < len(shot_explosion_frames):
                    explosion_frame = shot_explosion_frames[explosion_index]
                    explosion_rect = explosion_frame.get_rect(center=explosion["position"])
                    screen.blit(explosion_frame, explosion_rect.topleft)
                else:
                    explosion["active"] = False  # Mark the explosion as done
        shot_explosions = [explosion for explosion in shot_explosions if explosion["active"]]

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