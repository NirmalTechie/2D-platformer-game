import pygame

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer")

# Load assets (optional)
player_img = pygame.Surface((40, 60))
player_img.fill(BLUE)

# Define Player Class
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_y = 0
        self.on_ground = False

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

    def jump(self, keys):
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

    def apply_gravity(self, platforms):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Collision with the ground
        for platform in platforms:
            if self.rect.colliderect(platform):
                self.rect.bottom = platform.top
                self.vel_y = 0
                self.on_ground = True

# Create platforms
platforms = [pygame.Rect(200, 500, 400, 20)]  # Ground platform

# Create player instance
player = Player(300, 400)

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move(keys)
    player.jump(keys)
    player.apply_gravity(platforms)

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, (0, 255, 0), platform)

    # Draw player
    screen.blit(player_img, player.rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
