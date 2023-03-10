
import pygame
import random

pygame.init()

# Set up the display
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shooter Game")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Set up the player
player_width = 50
player_height = 50
player_x = width // 2 - player_width // 2
player_y = height - player_height
player_speed = 5

# Set up the enemy
enemy_width = 50
enemy_height = 50
enemy_x = random.randint(0, width - enemy_width)
enemy_y = 0
enemy_speed = 3
fps_clock = pygame.time.Clock()

# Set up the bullets
bullet_width = 5
bullet_height = 10
bullet_x = player_x + player_width // 2 - bullet_width // 2
bullet_y = player_y - bullet_height
bullet_speed = 10
bullet_state = "ready"

score = 0
game_font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)
game_over_text = game_over_font.render("Game Over", True, red)
game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))
game_over = False
difficulty = 1
start_screen = True

clock = pygame.time.Clock()

# Start screen loop
while start_screen:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_screen = False

    # Draw the game objects
    screen.fill(white)

    start_text = game_over_font.render("Click to Start", True, black)
    start_rect = start_text.get_rect(center=(width // 2, height // 2))
    screen.blit(start_text, start_rect)

    pygame.display.update()

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y - bullet_height
                bullet_state = "fire"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                game_over = False
                score = 0
                enemy_speed = 3
                player_speed = 5
                difficulty = 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < width - player_width:
        player_x += player_speed

    if bullet_state == "fire":
        bullet_y -= bullet_speed
        if bullet_y < 0:
            bullet_state = "ready"

    enemy_y += enemy_speed
    if enemy_y > height:
        enemy_x = random.randint(0, width - enemy_width)
        enemy_y = 0
        score += 1
        if score % 10 == 0:
            difficulty += 1
            enemy_speed += 1
            player_speed += 1

    if not game_over:
        if bullet_state == "fire" and bullet_x < enemy_x + enemy_width and bullet_x + bullet_width > enemy_x and bullet_y < enemy_y + enemy_height and bullet_y + bullet_height > enemy_y:
            bullet_state = "ready"
            enemy_x = random.randint(0, width - enemy_width)
            enemy_y = 0
            score += 10
            if score % 10 == 0:
                difficulty += 1
                enemy_speed += 1

        # Check for game over
        if enemy_y + enemy_height > player_y:
            game_over = True
            game_over_text = game_over_font.render("Game Over! Press any key to restart", True, red)
            game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))

    # Draw the game objects
    screen.fill(white)

    pygame.draw.rect(screen, black, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, red, (enemy_x, enemy_y, enemy_width, enemy_height))

    if bullet_state == "fire":
        pygame.draw.rect(screen, black, (bullet_x, bullet_y, bullet_width, bullet_height))

    score_text = game_font.render("Score: " + str(score), True, black)
    screen.blit(score_text, (10, 10))

    difficulty_text = game_font.render("Difficulty: " + str(difficulty), True, black)
    screen.blit(difficulty_text, (10, 40))

    if game_over:
        screen.blit(game_over_text, game_over_rect)
        
    fps = fps_clock.get_fps()
    fps_text = game_font.render("FPS: " + str(int(fps)), True, black)
    screen.blit(fps_text, (10, 70))

    # Update the display and tick the clock
    pygame.display.update()
    fps_clock.tick(60)

    pygame.display.update()

    # Restart the game if game over
    if game_over and pygame.key.get_pressed():
        game_over = False
        score = 0
        enemy_speed = 3
        player_speed = 5
        difficulty = 1
        

