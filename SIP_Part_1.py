import math 
import random 
import pygame 

s_width = 700
s_height = 500

player_start_x = 370
player_start_y = 300

enemy_start_y_min = 50
enemy_start_y_max = 150

enemy_speed_x = 4
enemy_speed_y = 40

arrow_speed_y = 10

collision_distance = 27

pygame.init()

screen = pygame.display.set_mode((s_width, s_height))
bg_image = pygame.image.load("White.jpg")
pygame.display.set_caption("Space Invader Game")
icon = pygame.image.load("Penguin.jpg")
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load("UFO.jpg")
player_x = player_start_x
player_y = player_start_y
player_x_change = 0

# Enemy
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_num = 15

for I in range(enemy_num):
    enemy_image.append(pygame.image.load("Alien.png"))
    enemy_x.append(random.randint(0, s_width - 64))
    enemy_y.append(random.randint(enemy_start_y_min, enemy_start_y_max))
    enemy_x_change.append(enemy_speed_x)
    enemy_y_change.append(enemy_speed_y)

# Arrow
arrow_image = pygame.image.load("Arrow.png")
arrow_x = 0
arrow_y = player_start_y
arrow_x_change = 0
arrow_y_change = arrow_speed_y
arrow_state = "ready"

# Score
score_value = 0
font = pygame.font.SysFont("Freestyle Script", 30)
text_x = 10
text_y = 10

over_font = pygame.font.SysFont("Kristen ITC", 70)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_image, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

def fire_bullet(x, y):
    global arrow_state
    arrow_state = "fire"
    screen.blit(arrow_image, (x + 16, y + 10))

def isCollision(enemy_x, enemy_y, arrow_x, arrow_y):
    distance = math.sqrt((enemy_x - arrow_x) ** 2 + (enemy_y - arrow_y) ** 2)

    return distance < collision_distance

running = True

while running:

    screen.fill((0, 0, 0))

    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5

            if event.key == pygame.K_RIGHT:
                player_x_change = 5

            if event.key == pygame.K_SPACE and bullet_state == "ready":
                arrow_x = player_x
                fire_bullet(arrow_x, arrow_y)

        if event.type == pygame.KEYUP and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            player_x_change = 0

    player_x += player_x_change

    player_x = max(0, min(player_x, s_width - 64)) 

    for i in range(enemy_num):
        if enemy_y[i] > 340: 
            for j in range(enemy_num):
                enemy_y[j] = 2000
                game_over_text()

            break

        enemy_x[i] += enemy_x_change[i]

        if enemy_x[i] <= 0 or enemy_x[i] >= s_width - 64:
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change[i]


        if isCollision(enemy_x[i], enemy_y[i], arrow_x, arrow_y):
            arrow_y = player_start_y
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, s_width - 64)
            enemy_y[i] = random.randint(enemy_start_y_min, enemy_start_y_max)
            enemy(enemy_x[i], enemy_y[i], i)

    if arrow_y <= 0:
        arrow_y = player_start_y
        arrow_state = "ready"

    elif arrow_state == "fire":
        fire_bullet(arrow_x, arrow_y)
        arrow_y -= arrow_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)

    pygame.display.update()