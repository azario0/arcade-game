import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Alien Shooter")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player
player_width = 50
player_height = 30
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 5

# Bullet
bullet_size = 5
bullets = []

# Aliens
alien_width = 40
alien_height = 30
aliens = []
alien_speed = 1

# Game variables
clock = pygame.time.Clock()
game_over = False
score = 0

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height))
    pygame.draw.polygon(screen, GREEN, [(x + player_width // 2, y), (x, y + player_height), (x + player_width, y + player_height)])

def draw_bullet(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, bullet_size, bullet_size))

def draw_alien(x, y):
    pygame.draw.rect(screen, RED, (x, y, alien_width, alien_height))
    pygame.draw.circle(screen, WHITE, (x + alien_width // 4, y + alien_height // 2), 5)
    pygame.draw.circle(screen, WHITE, (x + 3 * alien_width // 4, y + alien_height // 2), 5)

def show_score():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def show_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    
    font = pygame.font.Font(None, 36)
    text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 + 50))

def reset_game():
    global player_x, bullets, aliens, game_over, score
    player_x = width // 2 - player_width // 2
    bullets = []
    aliens = []
    game_over = False
    score = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not game_over:
                bullets.append([player_x + player_width // 2 - bullet_size // 2, player_y])
            elif event.key == pygame.K_r and game_over:
                reset_game()
            elif event.key == pygame.K_q and game_over:
                running = False

    if not game_over:
        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_width:
            player_x += player_speed

        # Move bullets
        bullets = [[x, y - 5] for x, y in bullets if y > 0]

        # Spawn aliens
        if random.randint(1, 60) == 1:
            aliens.append([random.randint(0, width - alien_width), 0])

        # Move aliens
        aliens = [[x, y + alien_speed] for x, y in aliens if y < height]

        # Check for collisions
        for bullet in bullets[:]:
            for alien in aliens[:]:
                if (alien[0] < bullet[0] < alien[0] + alien_width and
                    alien[1] < bullet[1] < alien[1] + alien_height):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    score += 1
                    break

        # Check if aliens reached the player
        for alien in aliens:
            if alien[1] + alien_height > player_y:
                game_over = True

    # Clear the screen
    screen.fill(BLACK)

    if not game_over:
        # Draw everything
        draw_player(player_x, player_y)
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])
        for alien in aliens:
            draw_alien(alien[0], alien[1])
        show_score()
    else:
        show_game_over()

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(60)

pygame.quit()