SCREEN_WIDTH = 1280 *2
SCREEN_HEIGHT = 720 *2

ASTEROID_MIN_RADIUS = 25
ASTEROID_KINDS = 5
ASTEROID_SPAWN_RATE = 0.8 #seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ACCEL_FACTOR = 1.2
MAX_ASTEROIDS = 50
ASTEROID_SPAWN_OFFSET = ASTEROID_MAX_RADIUS * 10

PLAYER_RADIUS = 60
PLAYER_TURN_SPEED = 300
PLAYER_MAX_SPEED = 225
PLAYER_ACCELERATION = 300
PLAYER_DECELERATION = 50
SHOT_RADIUS = 15
PLAYER_SHOOT_SPEED = 700
PLAYER_SHOT_COOLDOWN = 0.2

FRAME_DURATION = 100

PLAYER_IMAGE = "graphics/player.png"
BULLET_IMAGE = "graphics/OrangeScale__000.png"
AFTER_BURNER_FRAMES = ["graphics/blue_afterburner00.png",
                       "graphics/blue_afterburner01.png",
                       "graphics/blue_afterburner02.png",
                       "graphics/blue_afterburner03.png",]
ASTEROID_IMAGES = [("graphics/asteroid1.png", 1),
                   ("graphics/asteroid2.png", 2),
                   ("graphics/asteroid3.png", 3),
                   ("graphics/asteroid4.png", 4),]