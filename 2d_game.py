import pygame
import random
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.4

# Colors (Black & White theme)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLACK)
        pygame.draw.rect(self.image, GRAY, (5, 5, 30, 50))
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT - 100))
        self.vel_y = 0
        self.jumping = False
        self.speed = 6
        self.score = 0  # Added score system

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.jumping = False
                
        # Jumping
        if keys[pygame.K_SPACE] and not self.jumping:
            self.vel_y = -10
            self.jumping = True
        
        # Keep within screen bounds
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(topleft=(x, y))

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, GRAY, (10, 10), 10)
        self.rect = self.image.get_rect(center=(x, y))

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, GRAY, (15, 15), 15)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.speed = 2

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1

# Create groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create platforms
base_platform = Platform(0, HEIGHT - 40, WIDTH, 40)
platforms.add(base_platform)
all_sprites.add(base_platform)

for _ in range(4):  # More platforms for variety
    plat = Platform(random.randint(50, WIDTH - 150), random.randint(300, HEIGHT - 200), 150, 20)
    platforms.add(plat)
    all_sprites.add(plat)

# Create enemies
for _ in range(3):
    enemy = Enemy(random.randint(50, WIDTH - 50), random.randint(300, HEIGHT - 200))
    enemies.add(enemy)
    all_sprites.add(enemy)

# Create coins
for _ in range(5):
    coin = Coin(random.randint(50, WIDTH - 50), random.randint(100, HEIGHT - 100))
    coins.add(coin)
    all_sprites.add(coin)

# Game loop
running = True
while running:
    clock.tick(FPS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update
    all_sprites.update()
    
    # Check for enemy collision
    if pygame.sprite.spritecollide(player, enemies, False):
        print("Game Over!")
        running = False
    
    # Check for coin collection
    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    player.score += len(collected_coins)
    
    # Draw background
    screen.fill(WHITE)
    all_sprites.draw(screen)
    
    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {player.score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

pygame.quit()
