from circleshape import *
from constants import *
import random
from sound.sound import *

asteroid_masks = {}
for asteroid_type in range(1, 5):
    asteroid_masks[asteroid_type] = {}
    masking_image = pygame.image.load(f"graphics/asteroid{asteroid_type}.png").convert_alpha()
    for size in range(1, ASTEROID_KINDS + 1):
        scaled_image = pygame.transform.scale(masking_image, ((size * ASTEROID_MIN_RADIUS) * 1.8, (size * ASTEROID_MIN_RADIUS) * 1.8))
        asteroid_masks[asteroid_type][size] = pygame.mask.from_surface(scaled_image)

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
        self.size_index = radius // ASTEROID_MIN_RADIUS
        asteroid_images = [
            ("graphics/asteroid1.png", 1),
            ("graphics/asteroid2.png", 2),
            ("graphics/asteroid3.png", 3),
            ("graphics/asteroid4.png", 4),
        ]
        random_rock = random.choice(asteroid_images)
        self.original_image = pygame.image.load(random_rock[0]).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (1.8 * radius, 1.8 * radius))
        self.velocity = pygame.Vector2(x, y)
        
        self.angle = pygame.Vector2(0, -1).angle_to(self.velocity)
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.mask = asteroid_masks[random_rock[1]][self.size_index]
        self.mask_image = self.mask.to_surface(setcolor=(0, 255, 0, 100), unsetcolor=(0, 0, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        
        
        # self.original_image = pygame.image.load("graphics/OrangeScale__000.png").convert_alpha()
        # self.image = pygame.transform.scale(self.original_image, (0.33 * radius, 1.05 * radius))
        # self.velocity = pygame.Vector2(x, y)
        
        # self.image = pygame.transform.rotate(self.image, angle)
        # self.mask =  pygame.mask.from_surface(self.image)
        # self.mask_image = self.mask.to_surface(setcolor=(0, 255, 0, 100), unsetcolor=(0, 0, 0, 0))
        # self.rect = self.image.get_rect(center=(x, y))


    def update(self, dt):
        self.position += (self.velocity * dt)
        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, (0, 255, 0), (int(self.position.x), int(self.position.y)), self.radius, 1)
        mask_position = (self.rect.x, self.rect.y)
        screen.blit(self.mask_image, mask_position)

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