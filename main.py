from code.GameManager import GameManager
from code.Animatronics import *

pygame.init()
pygame.mixer.init()

pygame.mouse.set_visible(False)

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

backgroundHalf = display.get_width()/2

timeFont = pygame.font.Font('static/OCRAM.ttf', int(display.get_width()/40))

background = pygame.image.load('static/room.jpg').convert_alpha()
background = pygame.transform.scale(background, (display.get_width()+backgroundHalf,
                                                 display.get_height()))

backgroundT = pygame.image.load('static/room1.png').convert_alpha()
backgroundT = pygame.transform.scale(backgroundT, (display.get_width()+backgroundHalf,
                                                  display.get_height()))

buzzingSound = pygame.mixer.Sound('static/buzzing.wav')
buzzingSound.set_volume(0.3)

ambience1 = pygame.mixer.Sound('static/audio1.wav')
ambience1.set_volume(0.1)
ambience2 = pygame.mixer.Sound('static/audio2.wav')
ambience2.set_volume(0.1)
ambience = [ambience1, ambience2]
curSound = None

winSound = pygame.mixer.Sound('static/winsound.wav')
winSound.set_volume(3)

doorSound = pygame.mixer.Sound('static/door.wav')
doorSound.set_volume(0.3)

lightsaberSound = pygame.mixer.Sound('static/flash.wav')
lightsaberSound.set_volume(0.3)

speedJumpscare = pygame.image.load('static/speedjump.jpg').convert_alpha()
speedJumpscare = pygame.transform.scale(speedJumpscare,
                                        (display.get_width(),
                                         display.get_height())).convert_alpha()
speedJumpscareSound = pygame.mixer.Sound('static/jumpscare.wav')
speedJumpscareSound.set_volume(1000000000.1000)

benJumpscareSound = pygame.mixer.Sound('static/benjumpscare.wav')
benJumpscareSound.set_volume(1000000000.1000)

hallway = pygame.image.load('static/hallway.png').convert_alpha()
hallway = pygame.transform.scale(hallway, (backgroundHalf, backgroundHalf/1.44)).convert_alpha()

display.blit(background, (0, 0))

buzzingSound.play()

gm = GameManager(display, speedJumpscareSound, speedJumpscare)

xOffSet = 0

speedSprite = pygame.image.load('static/speedidle.png').convert_alpha()
speed = BaseSpeed(speedSprite,
                  (display.get_width()/2.5, display.get_height()/2.5), 3, 2,
                  speedJumpscareSound, speedJumpscare, display)

whiteBenSprite = pygame.image.load('static/whiteben.png').convert_alpha()
whiteBenSprite = pygame.transform.scale(whiteBenSprite, (600, 800))
blackBenSprite = pygame.image.load('static/blackben.png').convert_alpha()
blackBenSprite = pygame.transform.scale(blackBenSprite, (700, 1000))
whiteBen = BaseBen(display.get_size(), whiteBenSprite, 3, 5, benJumpscareSound)
blackBen = BaseBen(display.get_size(), blackBenSprite, 2, 4, benJumpscareSound)

timer = Timer(0.1)
lightsOut = False

doorCloseTimeOut = Timer(1)

doorOpen = True
lightsaberWorking = False

oxygen = 100.0

oneHour = 22
currentHour = 0
beforeNextHour = Timer(oneHour)


def update_draw_current_hour():
    global currentHour
    global beforeNextHour

    beforeNextHour.update()

    if beforeNextHour.done:
        currentHour += 1
        beforeNextHour = Timer(oneHour)

    stringHour = str(currentHour) + ' am'
    if currentHour == 0:
        stringHour = '12 pm'

    renderedText = timeFont.render(stringHour, False, (255, 255, 255)).convert_alpha()

    display.blit(renderedText, (display.get_width()-display.get_width()/7,
                                display.get_height()/6))


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.mixer.get_busy():
                    if doorCloseTimeOut.done:
                        doorCloseTimeOut = Timer(1)
                        doorSound.play()
                        if doorOpen:
                            doorOpen = False
                        else:
                            doorOpen = True
            elif event.button == 3:
                if pygame.mixer.get_busy():
                    lightsaberSound.play()
                    lightsaberWorking = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                if pygame.mixer.get_busy():
                    lightsaberSound.play()
                    lightsaberWorking = False

    timer.update()
    doorCloseTimeOut.update()

    mousePos = pygame.mouse.get_pos()

    xOffSet = mousePos[0]-backgroundHalf/2

    speed.update(doorOpen)

    whiteBen.update()
    blackBen.update()

    if xOffSet < 0:
        xOffSet = 0
    if xOffSet > display.get_width()-backgroundHalf:
        xOffSet = display.get_width()-backgroundHalf

    if timer.done:
        display.blit(background, (0-xOffSet, 0))
        if doorOpen:
            display.blit(hallway, (display.get_width()/1.99-xOffSet, display.get_height()/4.5))
            if speed.attacking:
                display.blit(speed.sprite, (display.get_width()/1.5-xOffSet,
                                            display.get_height()/2.5))

            gm.draw_rect_alpha(display, (0, 0, 0, 220), (display.get_width()/1.99-xOffSet, display.get_height()/4.5,
                                                         backgroundHalf, backgroundHalf/1.44))
            display.blit(backgroundT, (0 - xOffSet, 0))
    if whiteBen.attacking:
        display.blit(whiteBen.sprite, (whiteBen.currentLocation[0]-xOffSet,
                                       whiteBen.currentLocation[1]))
    if blackBen.attacking:
        display.blit(blackBen.sprite, (blackBen.currentLocation[0]-xOffSet,
                                       blackBen.currentLocation[1]))
    if lightsaberWorking:
        gm.draw_rect_alpha(display, (255, 255, 255, 100), (0, 0, display.get_width(), display.get_height()))
        if blackBen.attacking:
            blackBen.sprite = pygame.transform.scale(blackBen.sprite, (display.get_width(),
                                                                       display.get_height())).convert_alpha()
            display.blit(blackBen.sprite, (0, 0))
            pygame.display.update()
            pygame.mixer.music.stop()
            buzzingSound.stop()
            if curSound:
                curSound.stop()
            blackBen.jumpscareSound.play()
            while True:
                if not pygame.mixer.get_busy():
                    quit()
        if whiteBen.attacking:
            whiteBen.attacking = False
            whiteBen.beforeKillTimer = None
            whiteBen.spawnTimer = Timer(random.randint(whiteBen.aggressive,
                                                       whiteBen.aggressive * 3))

    if whiteBen.attacking:
        if whiteBen.beforeKillTimer:
            if whiteBen.beforeKillTimer.done:
                whiteBen.sprite = pygame.transform.scale(whiteBen.sprite, (display.get_width(),
                                                                           display.get_height())).convert_alpha()
                display.blit(whiteBen.sprite, (0, 0))
                pygame.display.update()
                pygame.mixer.music.stop()
                buzzingSound.stop()
                if curSound:
                    curSound.stop()
                whiteBen.jumpscareSound.play()
                while True:
                    if not pygame.mixer.get_busy():
                        quit()

    if blackBen.beforeKillTimer:
        if blackBen.beforeKillTimer.done:
            blackBen.attacking = False
            blackBen.beforeKillTimer = None
            blackBen.spawnTimer = Timer(random.randint(blackBen.aggressive,
                                                       blackBen.aggressive * 3))

    if not pygame.mixer.get_busy():
        if not lightsOut:
            lightsOut = True
            lightsaberWorking = False
            timer = Timer(1)
            display.fill((0, 0, 0))
            pygame.display.update()
        if lightsOut:
            if curSound:
                curSound.stop()
                curSound = None
            if timer.doneProcent >= 50:
                lightsOut = False
                if random.randint(1, 2) == 1:
                    curSound = random.choice(ambience)
                    curSound.play()
                buzzingSound.play()

    gm.update_draw_oxygen(doorOpen)
    update_draw_current_hour()

    if currentHour == 6:
        pygame.mixer.music.stop()
        buzzingSound.stop()
        if curSound:
            curSound.stop()
        winSound.play()
        while True:
            if not pygame.mixer.get_busy():
                quit()

    if not lightsOut:
        pygame.display.update()
