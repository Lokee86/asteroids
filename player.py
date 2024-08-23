import pygame
from circleshape import CircleShape
from constants import *
from sound.sound import *

class Player(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.original_image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (1.3 * radius, 1.6 * radius))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation = 0
        self.acceleration = PLAYER_ACCELERATION  # Define this in your constants
        self.max_speed = PLAYER_MAX_SPEED  # Define this in your constants
        self.deceleration = PLAYER_DECELERATION  # Define this in your constants
        self.shot_cooldown = PLAYER_SHOT_COOLDOWN
        self.score = 0

        self.afterburner_frames = [pygame.image.load(frame).convert_alpha() for frame in AFTER_BURNER_FRAMES]
        self.afterburner_frames = [pygame.transform.scale(frame, (0.75 * radius, 0.5 * radius)) for frame in self.afterburner_frames]
        self.afterburner_active = False
        self.afterburner_frame_index = 0
        self.afterburner_animation_speed = 20  # Adjust as needed
        self.afterburner_timer = 0
        self.afterburner_offset = pygame.Vector2(0, 60)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt * -1)
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.apply_acceleration(dt)
            self.afterburner_active = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.apply_acceleration(dt * -1)
            self.afterburner_active = False
        else:
            self.apply_deceleration(dt)
            self.afterburner_active = False

        if keys[pygame.K_SPACE]:
            self.shoot((0, -40))

        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt
        if self.shot_cooldown < 0:
            self.shot_cooldown = 0

        # Update position based on velocity
        self.position += self.velocity * dt
        
        # Wrap around the screen horizontally
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH

        # Wrap around the screen vertically
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT

        self.rect.center = self.position

        # Rotate the player image
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.position)
        
        # Update the mask after rotation
        self.mask = pygame.mask.from_surface(self.image)

        # update the afterburner if active
        if self.afterburner_active:
            self.afterburner_timer += dt * self.afterburner_animation_speed
            if self.afterburner_timer >= 1:
                self.afterburner_frame_index = (self.afterburner_frame_index + 1) % len(self.afterburner_frames)
                if self.afterburner_frame_index == 0:
                    # Advance through the first two frames only once
                    self.afterburner_frame_index += 1
                else:
                    # Loop the remaining frames
                    self.afterburner_frame_index = 1 + (self.afterburner_frame_index - 1 + 1) % (len(self.afterburner_frames) - 1)
                self.afterburner_timer = 0

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        # Rotate image around its center
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.position)
    
    def apply_acceleration(self, dt):
        direction = pygame.Vector2(0, -1).rotate(-self.rotation)
        self.velocity += direction * self.acceleration * dt
        # Cap the speed to the max speed
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    def apply_deceleration(self, dt):
        if self.velocity.length() > 0:
            decel_vector = self.velocity.normalize() * self.deceleration * dt
            if decel_vector.length() > self.velocity.length():
                self.velocity = pygame.Vector2(0, 0)
            else:
                self.velocity -= decel_vector

    def draw(self, screen):
        # Draw the player's image
        screen.blit(self.image, self.rect)

        # Draw the afterburner if active
        if self.afterburner_active:
            # Get the current afterburner frame
            afterburner_image = self.afterburner_frames[self.afterburner_frame_index]

            # Rotate the afterburner image to match the player's rotation
            rotated_afterburner = pygame.transform.rotate(afterburner_image, self.rotation)

            # Calculate the offset for the afterburner (e.g., behind the player)
            offset_rotated = self.afterburner_offset.rotate(-self.rotation)

            # Calculate the position for the afterburner
            afterburner_position = self.position + offset_rotated

            # Create a rect for the rotated afterburner at the calculated position
            afterburner_rect = rotated_afterburner.get_rect(center=afterburner_position)
            screen.blit(rotated_afterburner, afterburner_rect)

        # Draw the green circle around the player's image for debugging
        #pygame.draw.circle(screen, (0, 255, 0), (int(self.position.x), int(self.position.y)), self.radius, 1)

    def shoot(self, position):
        if self.shot_cooldown <= 0:
            laser_sound.play()
            self.shot_cooldown += PLAYER_SHOT_COOLDOWN
            
            offset_vector = pygame.Vector2(position).rotate(-self.rotation)
            spawn_position = pygame.Vector2(self.position) + offset_vector

            shot = Shot(spawn_position.x, spawn_position.y, SHOT_RADIUS, self.rotation)
            
            shot_direction = pygame.Vector2(0, -1).rotate(-self.rotation)
            shot.velocity = shot_direction * PLAYER_SHOOT_SPEED

class Shot(CircleShape):
    def __init__(self, x, y, radius, angle):
        super().__init__(x, y, radius)
        self.original_image = pygame.image.load(BULLET_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (0.33 * radius, 1.05 * radius))
        self.velocity = pygame.Vector2(x, y)
        self.image = pygame.transform.rotate(self.image, angle)
        self.mask =  pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.position += (self.velocity * dt)
        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect)