# Waka Game
# Author: Caleb, Lahclan, Noah
# Date: 31.07.26

import pygame
import sys
import random

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLUE = (60, 120, 220)
YELLOW = (240, 220, 60)
RED = (220, 60, 60)
BROWN = (150, 75, 0)

font_large = pygame.font.SysFont(None, 72)
score_font = pygame.font.SysFont("Arial", 36)

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Waka Game")

# Bullets
bullet_speed = 8
bullet_width = 12
bullet_height = 20
SHOOT_DELAY = 15

# Enemies
enemy_width, enemy_height = 40, 40
enemy_speed = 3
SPAWN_DELAY = 45

# Health
MAX_HEALTH = 5
INVINCIBILITY_FRAMES = 60  # 1 second at 60 FPS


def draw_bullet(x, y):
    points = [
        (x, y - bullet_height),
        (x - bullet_width // 2, y),
        (x + bullet_width // 2, y),
    ]
    pygame.draw.polygon(screen, YELLOW, points)


def bullet_rect(bullet):
    x, y = bullet
    return pygame.Rect(x - bullet_width // 2, y - bullet_height, bullet_width, bullet_height)


def spawn_enemy(enemies):
    x = random.randint(0, WIDTH - enemy_width)
    y = -enemy_height
    enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))


def move_enemies(enemies):
    for enemy in enemies:
        enemy.y += enemy_speed


def check_bullet_enemy_collisions(bullets, enemies):
    global score
    bullets_to_remove = []
    enemies_to_remove = []

    for bullet in bullets:
        b_rect = bullet_rect(bullet)
        for enemy in enemies:
            if b_rect.colliderect(enemy):
                if bullet not in bullets_to_remove:
                    bullets_to_remove.append(bullet)
                if enemy not in enemies_to_remove:
                    enemies_to_remove.append(enemy)
                    score += 10

    for bullet in bullets_to_remove:
        bullets.remove(bullet)

    for enemy in enemies_to_remove:
        enemies.remove(enemy)


def draw_heart(x, y, size, filled):
    r = size // 4

    if filled:
        pygame.draw.circle(screen, RED, (x - r, y), r)
        pygame.draw.circle(screen, RED, (x + r, y), r)
    else:
        pygame.draw.circle(screen, RED, (x - r, y), r, 2)
        pygame.draw.circle(screen, RED, (x + r, y), r, 2)

    points = [
        (x - size // 2, y),
        (x + size // 2, y),
        (x, y + size // 2),
    ]
    if filled:
        pygame.draw.polygon(screen, RED, points)
    else:
        pygame.draw.polygon(screen, RED, points, 2)


def draw_hearts(health):
    size = 30
    padding = 12
    start_x = 15 + size // 2
    start_y = 15 + size // 2

    for i in range(MAX_HEALTH):
        x = start_x + i * (size + padding)
        draw_heart(x, start_y, size, filled=(i < health))


# Game state (previously created via a new_game() function)
player = pygame.Rect(392.5, 500, 20, 50)
player_speed = 5
bullets = []
enemies = []
shoot_cooldown = 0
spawn_cooldown = SPAWN_DELAY
health = MAX_HEALTH
invincible_timer = 0
score = 0

game_state = "playing"  # or "game_over"

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == "playing":
        keys = pygame.key.get_pressed()

        # Move player
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += player_speed

        # Keep player on screen
        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH
        if player.top < 0:
            player.top = 0
        if player.bottom > HEIGHT:
            player.bottom = HEIGHT

        # Shooting
        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        if keys[pygame.K_SPACE] and shoot_cooldown == 0:
            bullet_x = player.centerx
            bullet_y = player.top
            bullets.append([bullet_x, bullet_y])
            shoot_cooldown = SHOOT_DELAY

        # Update bullets
        for bullet in bullets:
            bullet[1] -= bullet_speed

        bullets = [b for b in bullets if b[1] > -bullet_height]

        # Spawn and move enemies
        if spawn_cooldown > 0:
            spawn_cooldown -= 1
        else:
            spawn_enemy(enemies)
            spawn_cooldown = SPAWN_DELAY

        move_enemies(enemies)
        check_bullet_enemy_collisions(bullets, enemies)

        # Player damage
        enemies_to_remove = []
        for enemy in enemies:
            hit_player = player.colliderect(enemy)
            hit_bottom = enemy.bottom >= HEIGHT

            if hit_player or hit_bottom:
                enemies_to_remove.append(enemy)
                if invincible_timer == 0:
                    health -= 1
                    invincible_timer = INVINCIBILITY_FRAMES

        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)

        if invincible_timer > 0:
            invincible_timer -= 1

        if health <= 0:
            game_state = "game_over"

    # Draw everything
    screen.fill((0, 0, 255))

    if invincible_timer == 0 or invincible_timer % 10 < 5:
        pygame.draw.rect(screen, BROWN, player)

    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1])

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    draw_hearts(health)

    # Score in corner
    score_surface = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (20, 60))

    if game_state == "game_over":
        overlay_text = font_large.render("GAME OVER", True, WHITE)
        overlay_rect = overlay_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        screen.blit(overlay_text, overlay_rect)

    pygame.display.flip()

    clock.tick(60)