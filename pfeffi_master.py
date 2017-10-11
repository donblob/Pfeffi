# 1 - Import library
import pygame
from pygame.locals import *
import math
import random

# 2 - Initialize the game
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos = [200, 300]
acc = [0, 0]
arrows = []
accuracy = ""
# add some enemies
badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 194
# Sound Mixer init
pygame.mixer.init()

# 3 - Load images
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/dirt.png")
castle = pygame.image.load("resources/images/Gta2_tanker.png")
arrow = pygame.image.load("resources/images/bullet.png")
# enemy
badguyimg1 = pygame.image.load("resources/images/skeleton2.png")
badguyimg2 = pygame.image.load("resources/images/badguy2.png")
badguyimg3 = pygame.image.load("resources/images/badguy3.png")
badguyimg4 = pygame.image.load("resources/images/badguy4.png")
badguyimg = badguyimg1
badguylst = [badguyimg1, badguyimg2, badguyimg3, badguyimg4]
# HUD
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
# WIN and game over
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# 3.1 - Load audio
hit = pygame.mixer.Sound("resources/audio/Grenade+2.wav")
enemy = pygame.mixer.Sound("resources/audio/Burp+3.wav")
shoot = pygame.mixer.Sound("resources/audio/Gun+357+Magnum.wav")
hit.set_volume(0.6)
enemy.set_volume(0.4)
shoot.set_volume(0.8)
# pygame.mixer.music.load('resources/audio/shoot.wav')
pygame.mixer.music.load('resources/audio/Emil-Bulls-Monogamy/01-calm-down.mp3')
pygame.mixer.music.queue('resources/audio/Emil-Bulls-Monogamy/03-water.mp3')
pygame.mixer.music.queue('resources/audio/Emil-Bulls-Monogamy/04-chickeria.mp3')
pygame.mixer.music.queue('resources/audio/Emil-Bulls-Monogamy/05-mirror-me.mp3')
pygame.mixer.music.queue('resources/audio/Emil-Bulls-Monogamy/06-moonchild.mp3')
pygame.mixer.music.queue('resources/audio/Emil-Bulls-Monogamy/07-hi-it-is-me-christ.mp3')
pygame.mixer.music.queue('resources/audio/Emil-Bulls-Monogamy/08-monogamy.mp3')
pygame.mixer.music.queue('resources/audio/Emil-Bulls-Monogamy/09-obstacles.mp3')
pygame.mixer.music.queue('resources/audio/Emil-Bulls-Monogamy/10-resurrected.mp3')
pygame.mixer.music.queue('resources/audio/Emil-Bulls-Monogamy/11-smells-like-rock-n-roll.mp3')
pygame.mixer.music.queue('resources/audio/Emil-Bulls-Monogamy/12-wheels-of-steel.mp3')
pygame.mixer.music.queue('resources/audio/Emil-Bulls-Monogamy/13-quit-night.mp3')
pygame.mixer.music.play(0, 0.0)
pygame.mixer.music.set_volume(0.25)

# 4 - keep looping through
running = 1
exitcode = 0
while running:
    badtimer -= 1
    # 5 - clear the screen before drawing it again
    screen.fill(0)
    # 6 - draw the screen elements (with a 100*100 picture)
#    for x in range(width/grass.get_width()+1):
#        for y in range(height/grass.get_height()+1):
#            screen.blit(grass,(x*100,y*100))

    screen.blit(grass, (0, 0))
    screen.blit(castle, (0, 100))
    screen.blit(castle, (0, 200))
    screen.blit(castle, (0, 300))
    screen.blit(castle, (0, 400))
#   screen.blit(player, (100,100))
# ohne Winkel    screen.blit(player, playerpos)
    # 6.1 - Set player position and rotation
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerpos[1]+32), position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)

    # 6.2 - Draw arrows
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0])*10
        vely = math.sin(bullet[0])*10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 800 or bullet[2] < -64 or bullet[2] > 600:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
    # 6.3 - Draw badgers
    if badtimer == 0:
        badguys.append([800, random.randint(50, 500)])
        # legt die Anzahl der Feinde fest
        badtimer = 100-(badtimer1*2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 += 1
    index = 0
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index)
        badguy[0] -= 2
        # 6.3.1 - Attack castle
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            hit.play()
            # gibt den Schaden an. Also minus 5 bis 20 HP
            healthvalue -= random.randint(5, 20)
            badguys.pop(index)
        # 6.3.2 - Check for collisions
        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0] += 1
                badguys.pop(index)
                arrows.pop(index1)
            index1 += 1
        # 6.3.3 - Next bad guy
        index += 1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)

    # 6.4 - Draw clock
    font = pygame.font.Font(None, 60)
    survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000)+":"+str((90000-pygame.time.get_ticks())/1000 % 60).zfill(2), True, (0, 0, 0))
    textRect = survivedtext.get_rect()
    textRect.topright = [770, 5]
    screen.blit(survivedtext, textRect)

    # 6.5 - Draw health bar
    screen.blit(healthbar, (5, 5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8, 8))

    # 7 - update the screen
    pygame.display.flip()

    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys[0] = True
            elif event.key == pygame.K_a:
                keys[1] = True
            elif event.key == pygame.K_s:
                keys[2] = True
            elif event.key == pygame.K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32), position[0]-(playerpos1[0]+26)), playerpos1[0]+32, playerpos1[1]+32])

    # 9 - Move player
    if keys[0]:
        playerpos[1] -= 2
    elif keys[2]:
        playerpos[1] += 2
    if keys[1]:
        playerpos[0] -= 2
    elif keys[3]:
        playerpos[0] += 2

    # 10 - Win/Lose check
    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitcode = 1
    if healthvalue <= 0:
        running = 0
        exitcode = 0
    if acc[1] != 0:
        accuracy = acc[0]*1.0/acc[1]*100
    else:
        accuracy = 0
# 11 - Win/lose display
if exitcode == 0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0, 0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0, 0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
