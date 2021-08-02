import pygame
import random
import math
from pygame import mixer

#Python interpreter HAS to be the 3.9.6 WINDOWS STORE version. 

#Initialize the program
pygame.init() #need this line in ANY game.

#Create the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('c:/Users/danya/Documents/Visual Studio Code Projects/Projects/spaceInvaderGame/background.png')

#Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('c:/Users/danya/Documents/Visual Studio Code Projects/Projects/spaceInvaderGame/spaceship-icon.png')
pygame.display.set_icon(icon)

# Sound
mixer.music.load("c:/Users/danya/Documents/Visual Studio Code Projects/Projects/spaceInvaderGame/backgroundmusic.wav")
mixer.music.play(-1)
 

#Player
playerImg = pygame.image.load('c:/Users/danya/Documents/Visual Studio Code Projects/Projects/spaceInvaderGame/playership.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('c:/Users/danya/Documents/Visual Studio Code Projects/Projects/spaceInvaderGame/enemy1.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4) #(pre-wall-collision natural distance change)
    enemyY_change.append(40) #(pre-wall-collision natural distance change)

#Bullet
    # Ready -> You can't see the bullet on the screen
    # Fire -> The bullet is currently moving
bulletImg = pygame.image.load('c:/Users/danya/Documents/Visual Studio Code Projects/Projects/spaceInvaderGame/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0 #zero bc no horizontal movement of bullet. 
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y):
    screen.blit(enemyImg[i], (x,y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))



# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)



#GAME LOOP (Most important part of code)
running = True
while running: 
    screen.fill((230,230,250)) #set RGB screen bckgrd color, needs to be done above everything
    # Background Image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get(): #all 'events' should b under this for loop.
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether it's right or left.
        if event.type == pygame.KEYDOWN: #(means key pressed, in either direction).
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("c:/Users/danya/Documents/Visual Studio Code Projects/Projects/spaceInvaderGame/laser.wav")
                    bulletSound.play()
                    # Now, Get the current x co-ordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                
            
        if event.type == pygame.KEYUP: #(means key released).
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #Checking for boundaries of spaceship so it doesn't go Out of Bounds.
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy Movement (Post-Collision With SCreen Borders)
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4 #bump = move in the opposite direction
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4 #bump, then move in opp direction. 
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("c:/Users/danya/Documents/Visual Studio Code Projects/Projects/spaceInvaderGame/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i]) #remember, this command only takes 2 parameters, not a 3rd one just called 'i'.

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textY, textY)
    pygame.display.update() #need this line in ANY game. 

#os.path.dirname