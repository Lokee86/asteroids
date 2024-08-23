import pygame
from circleshape import CircleShape
from constants import *
from sound.sound import *

class Player(CircleShape):
    def __init__(self, x, y, radius, image_path):
        super().__init__(x, y, radius)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (1.85 * radius, 1.85 * radius))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation = 0
        self.acceleration = PLAYER_ACCELERATION  # Define this in your constants
        self.max_speed = PLAYER_MAX_SPEED  # Define this in your constants
        self.deceleration = PLAYER_DECELERATION  # Define this in your constants
        self.shot_cooldown = PLAYER_SHOT_COOLDOWN
        self.score = 0  

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt * -1)
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.apply_acceleration(dt)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.apply_acceleration(dt, reverse=True)
        else:
            self.apply_deceleration(dt)

        if keys[pygame.K_SPACE]:
            self.shoot((0, -40))

        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt
        if self.shot_cooldown < 0:
            self.shot_cooldown = 0

        # Update position based on velocity
        self.position += self.velocity * dt
        self.rect.center = self.position

        # Rotate the player image
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.position)
        
        # Update the mask after rotation
        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        # Rotate image around its center
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.position)
    
    def apply_acceleration(self, dt, reverse=False):
        direction = pygame.Vector2(0, -1).rotate(-self.rotation)
        if reverse:
            direction = -direction
        
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

        # Draw the green circle around the player's image for debugging
        # pygame.draw.circle(screen, (0, 255, 0), (int(self.position.x), int(self.position.y)), self.radius, 1)

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
        self.original_image = pygame.image.load("graphics/OrangeScale__000.png").convert_alpha()
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