SCREEN_WIDTH = int(1280 *1.4)
SCREEN_HEIGHT = int(720 *1.3)

ASTEROID_MIN_RADIUS = 25
ASTEROID_KINDS = 5
ASTEROID_SPAWN_RATE = 1.5 #seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ACCEL_FACTOR = 1.2
MAX_ASTEROIDS = 25
ASTEROID_SPAWN_OFFSET = ASTEROID_MAX_RADIUS * 4

PLAYER_RADIUS = 45
PLAYER_TURN_SPEED = 250
PLAYER_MAX_SPEED = 500
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