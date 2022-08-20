import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surface = test_font.render(f"Score: {current_time}", False, text_color)
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 4
            screen.blit(snail_surface, obstacle_rect)
        return obstacle_list
    else:
        return []


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 48)
game_active = False
text_color = (64, 64, 64)
box_color = "#c0e8ec"
start_time = 0
score = 0

sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

title_surface = test_font.render("Robo Runner", False, "#EEEEEE")
title_rect = title_surface.get_rect(center=(400, 75))

instructions_surface = test_font.render("Press space bar to play", False, "#EEEEEE")
instructions_rect = instructions_surface.get_rect(center=(400, 330))

# Obstacles
snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(800, 300))

obstacle_rect_list = []

player_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_gravity = -22
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -22
            if event.type == obstacle_timer:
                obstacle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900, 1100), 300)))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = pygame.time.get_ticks()

    if game_active:
        # Background
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        if score > 0:
            score_message_surface = test_font.render(f"Game over! Score: {score}", False, "#EEEEEE")
            score_message_rect = score_message_surface.get_rect(center=(400, 330))
            screen.blit(score_message_surface, score_message_rect)
        else:
            screen.blit(instructions_surface, instructions_rect)

        screen.blit(title_surface, title_rect)

    pygame.display.update()
    clock.tick(60)
