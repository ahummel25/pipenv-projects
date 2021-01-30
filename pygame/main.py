import math
import os
import random
import sys

import pygame
from pygame import mixer

from utils.files import find_data_file

# Intialize the pygame
pygame.init()

# create the screen
screen = ""

# Background
background = ""

# Caption and Icon
pygame.display.set_caption("Space Invaders")

# Player
playerImg = ""
playerX = ""
playerY = ""
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = ""

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = ""
bulletX = ""
bulletY = ""
bulletX_change = ""
bulletY_change = ""
bullet_state = ""

# Score

score_value = ""
font = ""

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font("freesansbold.ttf", 64)


def init():
    global background
    global bulletImg
    global bullet_state
    global bulletX
    global bulletX_change
    global bulletY
    global bulletY_change
    global enemyImg
    global enemyX
    global enemyX_change
    global enemyY
    global enemyY_change
    global font
    global num_of_enemies
    global playerX
    global playerImg
    global playerX_change
    global playerY
    global score_value
    global screen
    global textX
    global testY

    # create the screen
    screen = pygame.display.set_mode((800, 600))

    # Background
    background_icon = find_data_file("background.png")
    background = pygame.image.load(background_icon)

    # Sound
    background_music = find_data_file("background.wav")
    mixer.music.load(background_music)
    mixer.music.play(-1)

    # Caption and Icon
    pygame.display.set_caption("Space Invader")
    ufo_icon = find_data_file("ufo.png")
    icon = pygame.image.load(ufo_icon)
    pygame.display.set_icon(icon)

    # Player
    player_icon = find_data_file("player.png")
    playerImg = pygame.image.load(player_icon)
    playerX = 370
    playerY = 480
    playerX_change = 0

    # Enemy
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6

    enemy_icon = find_data_file("enemy.png")

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load(enemy_icon))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

    # Bullet

    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving

    bullet_icon = find_data_file("bullet.png")
    bulletImg = pygame.image.load(bullet_icon)
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    # Score

    score_value = 0
    font = pygame.font.Font("freesansbold.ttf", 32)

    textX = 10
    testY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(
        math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2))
    )
    if distance < 27:
        return True
    else:
        return False


def start_game():
    init()

    global bullet_state
    global bulletX
    global bulletY
    global enemyX
    global enemyY
    global playerX
    global playerX_change
    global playerY
    global score_value

    laser_sound = find_data_file("laser.wav")
    explosion_sound = find_data_file("explosion.wav")

    # Game Loop
    running = True
    while running:

        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound(laser_sound)
                        bulletSound.play()
                        # Get the current x cordinate of the spaceship
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # 5 = 5 + -0.1 -> 5 = 5 - 0.1
        # 5 = 5 + 0.1

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound(explosion_sound)
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                    start_game()


start_game()
