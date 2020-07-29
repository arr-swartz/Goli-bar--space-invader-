import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))
running = True

mixer.music.load("background.wav")
mixer.music.play(-1)
background_img = pygame.image.load("background.jpg")

pygame.display.set_caption("Goli Bar")
icon = pygame.image.load("swastika.png")
pygame.display.set_icon(icon)

exit = False
score = 0
f1 = open("highest.txt","r")
high_score = int(f1.read())
f1.close()

player = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
plx_change = 0

enemy = []
enemyY = []
enemyX = []
enx_change = []
eny_change = []
no_of_enemy = 5

for i in range(no_of_enemy):
    enemy.append(pygame.image.load("evil.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,300))
    enx_change.append(3)
    eny_change.append(40)

bullet = pygame.image.load("bullet.png")
bulletX = playerX
bulletY = 480
bullet_state = "ready"
bullet_change = -10

view = pygame.font.Font("Mango Drink.ttf" ,32)
over = pygame.font.Font("Mango Drink.ttf" ,64)
textX = 10
textY = 10

def show_score(x ,y):
    score_view = view.render(" Score : "+str(score) ,True ,(0 ,200 ,0))
    screen.blit(score_view ,(x ,y))

def game_over():
    over_text = over.render("GAME OVER" ,True ,(255 ,0 ,0))
    create = view.render(" created by : Rasik" ,True ,(255 ,0 ,0))
    high = view.render(" High Score : "+str(high_score) ,True ,(255 ,0 ,0))
    screen.blit(over_text ,(200 ,250))
    screen.blit(create ,(400 ,400))
    screen.blit(high ,(600 ,100))

def play(x,y):
    screen.blit(player, (x ,y))

def enem(x,y,i):
    screen.blit(enemy[i], (x ,y))

def fire_bullet(x,y):
    screen.blit(bullet, (x+16 ,y+10))
    global bullet_state
    bullet_state = "fire"

def isCollision(bx ,by ,ex ,ey):
    dist  = math.sqrt(math.pow((ex - bx) ,2) + (math.pow((ey - by) ,2)))
    if dist <= 27:
        return True
    else:
        return False

while running:
    screen.fill((0,0,0))
    screen.blit(background_img ,(0 ,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                plx_change = -5
            if event.key == pygame.K_RIGHT:
                plx_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    fire_bullet(playerX,playerY)
                    bulletX = playerX
                    bulletY = playerY
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                plx_change = 0

    if not(exit):
        for i in range(no_of_enemy):
            enemyX[i] += enx_change[i]
            if enemyX[i] <= 0:
                enx_change[i] = 3
                enemyY[i] += eny_change[i]
            if enemyX[i] >= 736:
                enx_change[i] = -3
                enemyY[i] += eny_change[i]
            if enemyY[i] >= 500:
                enemyY[i] = random.randint(50,300)
            if isCollision(enemyX[i] ,enemyY[i] ,playerX ,playerY):
                exit = True
                break
            enem(enemyX[i] ,enemyY[i],i)

        if bullet_state == "fire":
            bulletY += bullet_change
            if bulletY > 0:
                fire_bullet(bulletX ,bulletY)
            else:
                bullet_state = "ready"

        for i in range(no_of_enemy):
            if isCollision(bulletX ,bulletY ,enemyX[i] ,enemyY[i]):
                explosion_sound = mixer.Sound("explosion.wav")
                explosion_sound.play()
                enemyX[i] = random.randint(0,735)
                enemyY[i] = random.randint(50,300)
                bullet_state = "ready"
                bulletX = playerX
                bulletY = playerY
                score += 10

        playerX += plx_change

        if playerX <= 0:
            playerX = 0
        if playerX >= 736:
            playerX = 736

        play(playerX ,playerY)
        show_score(textX ,textY)

    if exit:
        if score > high_score :
            high_score = score
            with open("highest.txt","w") as f1:
                f1.write(str(high_score))
        game_over()
        show_score(100 ,100)
    pygame.display.update()
