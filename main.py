import os
import pygame
import time
import random

pygame.init()

gray = (110,110,110)
black = (0, 0, 0)
white = (255,255,255)
brown = (179,171,235)
orange = (252,156,11)
choco = (210,105,30)
yellow = (255,255,0)
cyan = (0,255,255)
green = (0,150,0)
bright_green = (0,255,0)
red = (150,0,0)
bright_red = (255,0,0)
blue = (0,0,255)
thing_color = (220,0,0)

size = displayWidth, displayHeigth = 800, 600
gameDisplay = pygame.display.set_mode(size)
pygame.display.set_caption('Dodgy Ride')
clock = pygame.time.Clock()
gamerWidth = 80
gamerHeight = 115
muted = False
pause = False

### power - ups
points2x = False
invisible = False
getMissile = False
missileShot = False
getShot = False

crash_sound = pygame.mixer.Sound("Assets/Glass.wav")
powerup_start = pygame.mixer.Sound("Assets/power_up.wav")
powerup_end = pygame.mixer.Sound("Assets/laser_gun.wav")
m_launch = pygame.mixer.Sound("Assets/m_launch.wav")
explosion = pygame.mixer.Sound("Assets/explosion.wav")
pygame.mixer.music.load("Assets/Man.mp3")

doublePointsImg = pygame.image.load("Assets/2x_blue.png")
doublePointsImg = pygame.transform.scale(doublePointsImg, (80,80))
invisibleImg = pygame.image.load("Assets/inv.png")
invisibleImg = pygame.transform.scale(invisibleImg, (80,80))
missileImg = pygame.image.load("Assets/missile.png")
missileImg = pygame.transform.scale(missileImg, (100, 30))
straightMissile = pygame.image.load("Assets/missile_straight.png")
straightMissile = pygame.transform.scale(straightMissile, (20, 100))

bg = pygame.image.load("Assets/highway-half.png")
gameIcon = pygame.image.load("Assets/blue_car1.png")
pygame.display.set_icon(gameIcon)
carImg = pygame.image.load("Assets/blue_car1.png")
carImg = pygame.transform.scale(carImg,(gamerWidth,gamerHeight))
invCar = pygame.image.load("Assets/blue_car_transp.png")
invCar = pygame.transform.scale(invCar, (gamerWidth,gamerHeight))

redEnemy = pygame.image.load("Assets/red_car.png")
redEnemy = pygame.transform.scale(redEnemy,(gamerWidth,gamerHeight))
yellowEnemy = pygame.image.load("Assets/yellow_car.png")
yellowEnemy = pygame.transform.scale(yellowEnemy,(90,120))

def save_record(file_name,dodged):
    with open(file_name, 'r+') as f:
        if os.stat(file_name).st_size == 0:
            f.write(str(dodged))
            f.seek(0)

        else:
            oldRecord = int(f.read())
            f.seek(0)
            if dodged > oldRecord:
                newRecordDisplay(dodged)
                f.write(str(dodged))
                f.seek(0)

def clear_record():
    with open('Assets/highscore.txt', "w") as f:
        f.write(str(0))
        f.seek(0)

def newRecordDisplay(res):
    font = pygame.font.SysFont("arial",50)
    text = font.render("New Record: " + str(res), True, cyan)
    gameDisplay.blit(text, (250,150))

def showScore(score, dodged, rand, bonus_y):
    font = pygame.font.SysFont(None, 25)
    with open('Assets/highscore.txt','r') as rf:
        rec = rf.read()

    pygame.draw.rect(gameDisplay,yellow,[0,0,100,50])
    score_text = font.render("Score: " + str(score), True, black)
    record_text = font.render("Record: " + str(rec), True, blue)
    # dodged_text = font.render("Dodged: " + str(dodged), True, black)
    # randNum_text = font.render("Rand: " + str(rand), True, blue)
    # bonus_text = font.render("bonusY: " + str(bonus_y), True, blue)
    gameDisplay.blit(score_text,(5,5))
    gameDisplay.blit(record_text,(5,30))
    # gameDisplay.blit(randNum_text,(5,55))
    # gameDisplay.blit(bonus_text, (5, 75))
    # gameDisplay.blit(dodged_text,(5, 90))

def game_quit():
    pygame.quit()
    quit()

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def inv_car(x,y):
    gameDisplay.blit(invCar,(x,y))

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(message,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if (x + w) > mouse[0] > x and (y + h) > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_objects(message, smallText, black)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)

def mute():
    global muted
    muted = True

def unmute():
    global muted
    muted = False

def paused():
    pygame.mixer.music.pause()

    largeText = pygame.font.Font("freesansbold.ttf", 70)
    textSurf, textRect = text_objects("Paused", largeText,black)
    textRect.center = ((displayWidth / 2), (displayHeigth / 2))
    gameDisplay.blit(textSurf, textRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    unpaused()
                if event.key == pygame.K_p:
                    unpaused()

        #gameDisplay.fill(white)
        button("Continue", 150, 450, 100, 50, green, bright_green, unpaused)
        button("Quit", 550, 450, 100, 50, red, bright_red, game_quit)
        button("Clear record", 500,20,180,50, gray, white, clear_record)
        if muted == False:
            button("Mute", 690, 20, 90, 50, bright_red, yellow, mute)
        elif muted == True:
            button("Unmute", 690,20, 90, 50, green, yellow, unmute)

        pygame.display.update()
        clock.tick(20)

def unpaused():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def AABB(ax1, ay1, aw, ah, bx1, by1, bw, bh):
    ax2, ay2, bx2, by2 = ax1 + aw, ay1 + ah, bx1 + bw, by1 + bh
    return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1

# def shootMissile():
#     global missileShot
#     missileShot = True

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()

        gameDisplay.fill(orange)
        largeText = pygame.font.Font("freesansbold.ttf", 70)
        textSurf, textRect = text_objects("Dodgy Ride", largeText,black)
        textRect.center = ((displayWidth / 2), (displayHeigth / 2))
        gameDisplay.blit(textSurf, textRect)

        button("PLAY", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, game_quit)

        pygame.display.update()
        clock.tick(20)

def game_over():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)

    largeText = pygame.font.Font(None, 100)
    textSurf, textRect = text_objects("Game Over", largeText,black)
    textRect.center = ((displayWidth / 2), (displayHeigth / 2))
    gameDisplay.blit(textSurf, textRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # gameDisplay.fill(white)
        button("Play again", 150, 450, 110, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, game_quit)

        pygame.display.update()
        clock.tick(20)

def game_loop():
    global pause, muted, enemyImg, points2x, invisible, getMissile, missileShot
    muted = False
    bonusBlit = False
    points2x = invisible = getMissile = False

    if muted == False:
        pygame.mixer.music.play(-1)

    x = (displayWidth * 0.45)
    y = (displayHeigth * 0.8)
    missileX, missileY = -200,-80
    x_change = 0
    dodged = 0
    score = 0
    chooseEnemy = 0
    chooseBonus = 0
    #driver_speed = 13
    driver_speed = 500
    road_speed = 8
    #road_speed = 300
    l_x = 12
    r_x = 400
    u_y = 0
    d_y = 300
    n_y = -300
    k_right = False
    k_left = False

    enemy_startx = random.randrange(0, displayWidth)
    enemy_starty = -600
    enemy_speed = 8
    #enemy_speed = 400
    bonus_x = random.randrange(0, displayWidth - 60)
    bonus_y = -80
    bonusId = 0
    bonusTimer = 0

    gameDisplay.fill(black)
    gameDisplay.blit(bg, (12, 0))
    gameDisplay.blit(bg, (12, 300))
    gameDisplay.blit(bg, (400, 0))
    gameDisplay.blit(bg, (400, 300))
    gameExit = False

    while not gameExit:

        dt = clock.tick(120)
        dt /= 1000

        if muted:
            pygame.mixer.music.pause()
        if muted == False:
            pygame.mixer.music.unpause()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and getMissile:
                    getMissile = False
                    missileShot = True
                    missileX = x + 30
                    missileY = y
                    pygame.mixer.Sound.play(m_launch)
                if event.key == pygame.K_LEFT and x > 0:
                    k_left = True
                if event.key == pygame.K_RIGHT and x < (displayWidth-gamerWidth):
                    k_right = True
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    k_left = False
                    x_change = 0
                elif event.key == pygame.K_RIGHT:
                    k_right = False
                    x_change = 0

        if k_left:
            x_change = -driver_speed
        if k_right:
            x_change = driver_speed
        if k_left and k_right:
            x_change = 0

        x += (x_change * dt)

        gameDisplay.fill(black)
        gameDisplay.blit(bg, (l_x, n_y))
        gameDisplay.blit(bg, (r_x, n_y))
        gameDisplay.blit(bg, (l_x, u_y))
        gameDisplay.blit(bg, (r_x, u_y))
        gameDisplay.blit(bg, (l_x, d_y))
        gameDisplay.blit(bg, (r_x, d_y))
        u_y += (road_speed )
        d_y += (road_speed )
        n_y += (road_speed )
        if d_y >= 600:
            n_y -= 300
            u_y -= 300
            d_y -= 300

        if invisible:
            inv_car(x,y)
        else:
            car(x, y)

        if missileShot:
            gameDisplay.blit(straightMissile, (missileX, missileY))
            missileY -= 8

        if chooseEnemy == 0:
            gameDisplay.blit(redEnemy,(enemy_startx, int(enemy_starty)))
        if chooseEnemy == 1:
            gameDisplay.blit(yellowEnemy,(enemy_startx, int(enemy_starty)))
        if chooseBonus == 3 and not points2x:
            bonus_y = -80
            bonusBlit = True
            bonusId = 3
        if chooseBonus == 4 and not invisible:
            bonus_y = -80
            bonusBlit = True
            bonusId = 4
        if chooseBonus == 1 and not getMissile:
            bonus_y = -80
            bonusBlit = True
            bonusId = 1

        if bonusBlit:
            if bonusId == 3:
                gameDisplay.blit(doublePointsImg, (bonus_x, bonus_y))
            elif bonusId == 4:
                gameDisplay.blit(invisibleImg, (bonus_x, bonus_y))
            elif bonusId == 1:
                gameDisplay.blit(missileImg, (bonus_x, bonus_y))

        enemy_starty += (enemy_speed )

        if bonusBlit:
            bonus_y += (6)

        showScore(score, missileShot, chooseBonus, bonus_y)

        # if x > (displayWidth - gamerWidth) or x < 0:
        #     save_record('Assets/highscore.txt', score)
        #     game_over()
        if x > (displayWidth - gamerWidth):
            x = displayWidth - gamerWidth
        elif x < 0:
            x = 0

        if enemy_starty > displayHeigth:
            enemy_starty = 0 - gamerHeight
            enemy_startx = random.randrange(0, displayWidth - gamerWidth)
            chooseEnemy = random.randrange(0, 2)
            chooseBonus = random.randrange(0, 20)
            # if points2x or invisible:
            if bonusBlit:
                chooseBonus = 2

            dodged += 1
            if points2x:
                score += 2
            else:
                score += 1

            if dodged > 20:
                if dodged % 7:
                    enemy_speed += 0.5
                    #enemy_speed += 5
            else:
                enemy_speed += 0.3
                #enemy_speed += 3

        if bonus_y > displayHeigth:
            bonusBlit = False
            bonus_y = -80
            #chooseBonus = random.randrange(0, 5)

        if bonusTimer > 600:
            if points2x:
                points2x = False
                pygame.mixer.Sound.play(powerup_end)
            if invisible:
                invisible = False
                pygame.mixer.Sound.play(powerup_end)


        ### if crash in another car then game over
        #if y < enemy_starty + gamerHeight and enemy_starty < y + gamerHeight:
        #    if x + gamerWidth > enemy_startx and x < enemy_startx + gamerWidth:
        if not invisible:
            if AABB(x,y,gamerWidth,gamerHeight,enemy_startx,enemy_starty,gamerWidth,gamerHeight):
                save_record('Assets/highscore.txt', score)
                game_over()

        if AABB(x,y,gamerWidth,gamerHeight,bonus_x,bonus_y,80,80):
            bonus_y = - 80
            pygame.mixer.Sound.play(powerup_start)
            bonusTimer = 0
            bonusBlit = False
            if bonusId == 3:
                points2x = True
            elif bonusId == 4:
                invisible = True
            elif bonusId == 1:
                getMissile = True

        if AABB(missileX, missileY, 100, 20, enemy_startx,enemy_starty, gamerWidth, gamerHeight):
            missileShot = False
            enemy_starty = displayHeigth
            missileX,missileY = -200, -80
            pygame.mixer.Sound.play(explosion)
        if missileY < -100:
            missileShot = False
            missileX, missileY = -200, -80


        bonusTimer += 1
        pygame.display.update()
        # clock.tick(120)

game_intro()
game_loop()
pygame.quit()
quit()