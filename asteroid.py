from circleshape import *
from constants import *
import random
from sound import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        original_image = pygame.image.load("asteroid.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (2 * radius, 2 * radius))
        self.velocity = pygame.Vector2(x, y)
        angle = pygame.Vector2(0, -1).angle_to(self.velocity)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=(x, y))
        

    def update(self, dt):
        self.position += (self.velocity * dt)
        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def split(self):
        self.kill()
        rock_death.play()
        if self.radius == ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(5, 75)
        new_velocity1 = self.velocity.rotate(random_angle)
        new_velocity2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = new_velocity1 * ACCEL_FACTOR
        asteroid2.velocity = new_velocity2 * ACCEL_FACTOR