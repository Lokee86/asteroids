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
        self.shot_cooldown = PLAYER_SHOT_COOLDOWN
        self.score = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt * -1)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(dt * -1)
        if keys[pygame.K_SPACE]:
            self.shoot(self.position)

        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt
        if self.shot_cooldown < 0:
            self.shot_cooldown = 0

        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = self.position
        
        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        # Rotate image around its center
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def move(self, dt):
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def shoot(self, position):
        if self.shot_cooldown <= 0:
            laser_sound.play()
            self.shot_cooldown += PLAYER_SHOT_COOLDOWN
            shot = Shot(position.x, position.y, SHOT_RADIUS, self.rotation)
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