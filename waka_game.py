# Waka Game
# Author: Caleb, Lachlan, and Noah
# Date: 28.07.26

import pygame, sys

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Waka Game")

player = pygame.Rect(392.5,700,20,50)
player_speed = 5

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit

    screen.fill((0,0,255))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += player_speed

    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH
    if player.top < 0:
        player.top = 0
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT

    pygame.draw.rect(screen,(150,75,0), player)
    pygame.display.flip()

    clock.tick(60)
