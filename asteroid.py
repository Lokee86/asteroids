from circleshape import *
from constants import *
import random
from sound.sound import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
        self.size_index = radius // ASTEROID_MIN_RADIUS
        random_rock = random.choice(ASTEROID_IMAGES)
        self.original_image = pygame.image.load(random_rock[0]).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (1.8 * radius, 1.8 * radius))
        self.velocity = pygame.Vector2(x, y)
        
        self.angle = pygame.Vector2(0, -1).angle_to(self.velocity)
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(x, y))


    def update(self, dt):
        self.position += (self.velocity * dt)
        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # Draw the green circle around the asteroid image for debugging
        # pygame.draw.circle(screen, (0, 255, 0), (int(self.position.x), int(self.position.y)), self.radius, 1)


    def split(self):
        self.kill()
        rock_death.play()
        if self.radius == ASTEROID_MIN_RADIUS:
            return 10
        random_angle = random.uniform(5, 75)
        new_velocity1 = self.velocity.rotate(random_angle)
        new_velocity2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = new_velocity1 * ACCEL_FACTOR
        asteroid2.velocity = new_velocity2 * ACCEL_FACTOR
        return int(10 * (self.radius / ASTEROID_MIN_RADIUS))