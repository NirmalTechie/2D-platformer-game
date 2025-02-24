import pygame
import os

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLAYER_SPEED = 5
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LAVA_COLOR = (255, 69, 0)
FONT = pygame.font.Font(None, 36)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer with Animations & Hazards")

# Load Sounds
jump_sound = pygame.mixer.Sound("jump.wav")
goal_sound = pygame.mixer.Sound("goal.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

# Load Background Music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Loop indefinitely

# Load High Scores
SCORE_FILE = "highscores.txt"

def load_high_scores():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            return [int(score) for score in file.readlines()]
    return []

def save_high_score(score):
    scores = load_high_scores()
    scores.append(score)
    scores.sort(reverse=True)
    with open(SCORE_FILE, "w") as file:
        file.writelines([str(s) + "\n" for s in scores[:5]])

# Load Player Animations
player_standing = pygame.image.load("player_stand.png")
player_jumping = pygame.image.load("player_jump.png")
player_img = player_standing

# Player Class
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_y = 0
        self.on_ground = False
        self.score = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

    def jump(self, keys):
        global player_img
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            jump_sound.play()
            player_img = player_jumping  # Switch to jumping animation

    def apply_gravity(self, platforms):
        global player_img
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        for platform in platforms:
            if self.rect.colliderect(platform):
                self.rect.bottom = platform.top
                self.vel_y = 0
                self.on_ground = True
                player_img = player_standing  # Switch to standing animation

# Enemy Class (Moving Hazard)
class Enemy:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = speed
        self.direction = 1  # 1 = right, -1 = left

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < 100 or self.rect.x > 700:
            self.direction *= -1  # Reverse direction

# Falling Platform Class
class FallingPlatform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 20)
        self.falling = False

    def update(self, player):
        if self.rect.colliderect(player.rect):
            self.falling = True
        if self.falling:
            self.rect.y += 3  # Falls downward

# Define Levels
levels = {
    "Easy": {
        "platforms": [pygame.Rect(200, 500, 400, 20)],
        "goal": pygame.Rect(700, 450, 40, 40),
        "enemies": [Enemy(400, 460, 2)],
        "spikes": [pygame.Rect(300, 550, 50, 20)],
        "falling_platforms": [],
        "lava": []
    },
    "Medium": {
        "platforms": [pygame.Rect(100, 500, 200, 20), pygame.Rect(400, 400, 200, 20)],
        "goal": pygame.Rect(700, 350, 40, 40),
        "enemies": [Enemy(450, 360, 3)],
        "spikes": [pygame.Rect(250, 550, 50, 20)],
        "falling_platforms": [FallingPlatform(500, 350)],
        "lava": []
    },
    "Hard": {
        "platforms": [pygame.Rect(50, 500, 150, 20), pygame.Rect(250, 400, 150, 20), pygame.Rect(450, 300, 150, 20)],
        "goal": pygame.Rect(700, 250, 40, 40),
        "enemies": [Enemy(500, 260, 4)],
        "spikes": [pygame.Rect(350, 550, 50, 20)],
        "falling_platforms": [FallingPlatform(300, 450)],
        "lava": [pygame.Rect(200, 580, 400, 20)]
    }
}

# Start Menu
def start_menu():
    screen.fill(WHITE)
    title = FONT.render("Choose Difficulty:", True, BLACK)
    easy_text = FONT.render("1. Easy", True, BLACK)
    medium_text = FONT.render("2. Medium", True, BLACK)
    hard_text = FONT.render("3. Hard", True, BLACK)

    screen.blit(title, (WIDTH // 3, HEIGHT // 3))
    screen.blit(easy_text, (WIDTH // 3, HEIGHT // 3 + 40))
    screen.blit(medium_text, (WIDTH // 3, HEIGHT // 3 + 80))
    screen.blit(hard_text, (WIDTH // 3, HEIGHT // 3 + 120))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "Easy"
                if event.key == pygame.K_2:
                    return "Medium"
                if event.key == pygame.K_3:
                    return "Hard"

# Game Setup
difficulty = start_menu()
level_data = levels[difficulty]
player = Player(100, 400)
enemies = level_data["enemies"]
falling_platforms = level_data["falling_platforms"]
running = True
clock = pygame.time.Clock()

# Game Loop
while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move(keys)
    player.jump(keys)
    player.apply_gravity(level_data["platforms"])

    # Draw Platforms
    for platform in level_data["platforms"]:
        pygame.draw.rect(screen, GREEN, platform)

    # Update and Draw Falling Platforms
    for f_platform in falling_platforms:
        f_platform.update(player)
        pygame.draw.rect(screen, (200, 100, 50), f_platform.rect)

    # Draw Lava
    for lava in level_data["lava"]:
        pygame.draw.rect(screen, LAVA_COLOR, lava)
        if player.rect.colliderect(lava):
            hit_sound.play()
            player.rect.x, player.rect.y = 100, 400  # Reset position

    # Move and Draw Enemies
    for enemy in enemies:
        enemy.move()
        pygame.draw.rect(screen, (255, 0, 0), enemy.rect)

    # Draw Player
    screen.blit(player_img, player.rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
