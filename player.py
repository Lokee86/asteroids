import pygame
from circleshape import CircleShape
from constants import *

class Player(CircleShape):
    def __init__(self, x, y, radius, image_path):
        super().__init__(x, y, radius)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (2 * radius, 2 * radius))
        self.image = self.original_image  # Store the original image to avoid degradation over transformations
        self.rect = self.image.get_rect(center=(x, y))
        self.rotation = 0

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
        
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
    
        self.rect.center = self.position

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

