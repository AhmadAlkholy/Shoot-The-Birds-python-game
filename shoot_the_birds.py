import pygame
import time
import random

pygame.init()

score = 0
displayWidth = 1300
displayHeight = 700
bullets = 5
LEFT = 1
RIGHT = 3
gameExit = False
level = 1

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight), pygame.FULLSCREEN)  # the frame of the game with it's size as toople in parameter
infoObject = pygame.display.Info()
displayWidth = infoObject.current_w
displayHeight = infoObject.current_h
pygame.font.init()

now = time.time
rand = random.randint
scale = pygame.transform.scale


def img(path, scale=0):
    img = pygame.image.load(path)
    if scale:
        img = pygame.transform.scale(img, scale)
    return img


# Setting Images
background = img('images/background.jpg', (displayWidth, displayHeight))  # loads image from path
background2 = img('images/background2.jpg', (displayWidth, displayHeight))  # loads image from path
target = img('images/target.png', (50, 50))
target2 = img('images/target2.png', (50, 50))
bullet = img('images/bul.png', (round(displayWidth * .035), round(displayWidth * .12)))

timer_time = now()
game_time = 60


def timer():
    global level
    global gameExit
    global timer_time
    global game_time
    if now() - timer_time > 1:
        game_time -= 1
        timer_time = now()
    if game_time == 0:
        hall_of_fame()
        return False
    elif game_time == 50:
        level = 2
    elif game_time == 35:
        level = 3
    display_message(str(game_time), (displayWidth - 70, 20), 50)


# bird waving image
birdsFrames = [[], [], []]
for t in range(5):
    birdsFrames[0].append(img('images/frame_00' + str(t) + '.png', (100, 75)))
    birdsFrames[1].append(img('images/frame_00' + str(t) + '.png', (66, 50)))
    birdsFrames[2].append(img('images/frame_00' + str(t) + '.png', (50, 40)))

fly_time = now()
l = 0
dir = 1


def bird_wave(x, y, flip, size):
    global fly_time, l, dir
    birdy = birdsFrames[size][l]

    if flip == -1:
        birdy = pygame.transform.flip(birdsFrames[size][l], True, False)
    gameDisplay.blit(birdy, (x, y))
    if now() - fly_time > .1:
        if dir == 1:
            l += 1
        else:
            l -= 1
        fly_time = now()
        if l == 0:
            dir = 1
        elif l == 4:
            dir = 0


pygame.display.set_caption('Shoot The Birds')

white = (255, 255, 255)
transparent = (0, 0, 0, 0)

clock = pygame.time.Clock()


def targetMove():
    mousePosition = pygame.mouse.get_pos()
    gameDisplay.blit(target, (
        mousePosition[0] - 25, mousePosition[1] - 25))  # positions carImg related to game display width & height


birdX = 0
birdTime = now()
birds2 = []


def birdMove():
    global birdX
    global birds2
    global birdTime
    right = rand(0, 1)
    d = 1
    for birdz in birds2:
        if birdz[0] < -50 or birdz[0] > displayWidth + 50:
            birds2.remove(birdz)
            continue
        birdz[0] += 3 * birdz[2]
        bird_wave(birdz[0], birdz[1], birdz[2], birdz[3])
    if right:
        pos = displayWidth + 50
        d = -1
    else:
        pos = -50
        d = 1
    if now() - birdTime > rand(1, 5) and len(birds2) < 15:
        size = rand(1, level) - 1
        Y = displayHeight * rand(1, 10) * .05
        birds2.append([pos, Y, d, size])
        birdTime = now()


def display_message(text, cord, font=20, color=(200, 30, 30)):
    textFont = pygame.font.Font('fonts/FreeSansBold.ttf', font)  # font family &size
    textsurface = textFont.render(text, False, color)
    gameDisplay.blit(textsurface, cord)


def text_width(text, font):
    textFont = pygame.font.Font('fonts/FreeSansBold.ttf', font)
    return textFont.render(text, False, (0, 0, 0)).get_width()


message = False

music = pygame.mixer.music
music.load('sound_effects/music.mp3')
music.set_volume(.3)
music.play(0)

soundFile = pygame.mixer.Sound
shot = soundFile('sound_effects/43755__gezortenplotz__ar15-rifle03.wav')
empty_gun = soundFile('sound_effects/154934__klawykogut__empty-gun-shot.wav')
reload = soundFile('sound_effects/396331__nioczkus__1911-reload.aiff')


def sound(effect, volume=.5, times=0):
    effect.set_volume(volume)
    effect.play(times)


# sound('music.mp3',.2, -1)
sizes = [(100, 75), (60, 50), (50, 40)]
extras = [50, 100, 150]


def shoot(x, y):
    global score, bullets, message, birds2
    if bullets == 0:
        message = "you need to relood"
        sound(empty_gun, .5)

    else:
        gameDisplay.blit(target2, (x, y))
        bullets -= 1
        sound(shot, .1)
        for bird in birds2:
            x_limit = bird[0] + sizes[bird[3]][0]
            y_limit = bird[1] + sizes[bird[3]][1]
            if x > bird[0] and x < x_limit and y > bird[1] and y < y_limit:
                birds2.remove(bird)
                score += extras[bird[3]]
                # gameDisplay.blit(die , (bird[0], bird[1]) )


def screen_resize():
    global displayChange
    global background
    global background2
    global bullet
    if displayChange == True:
        background = scale(background, (displayWidth, displayHeight))
        background2 = scale(background2, (displayWidth, displayHeight))
        bullet = scale(bullet, (round(displayWidth * .035), round(displayWidth * .12)))
        displayChange = False


menu_dimentions = [(1000, 1000), (1000, 1000)]


def display_changing(event):
    global displayChange, displayWidth, displayHeight, menu_dimentions
    if event.type == pygame.VIDEORESIZE:
        scrsize = event.size
        displayWidth = event.w
        displayHeight = event.h
        displayChange = True
        pygame.display.set_mode(scrsize, pygame.FULLSCREEN)
        menu_dimentions = [((displayWidth - text_width('NEW GAME', 40)) * .5, displayHeight * .3),
                           # ( (displayWidth - text_width('HALL OF FAME',40)) *.5 , displayHeight*.4 ),
                           ((displayWidth - text_width('QUIT', 40)) * .5, displayHeight * .4)]


# making game loop
displayChange = False
mouseOut = True


def game_loop():
    global mouseOut
    global displayWidth
    global displayHeight
    global bullets
    global message
    global background
    global bullet
    global gameExit
    j = 0
    while not gameExit:  # if crashed is false

        screen_resize()

        gameDisplay.blit(background, (0, 0))

        birdMove()

        # displaying relood message
        if message != False:
            j += 1
            display_message(message, (10, 10))
            if j > 10:
                message = False
                j = 0
        if mouseOut:
            mousePosition = pygame.mouse.get_pos()
            targetMove()

        for j in range(bullets):
            gameDisplay.blit(bullet, (displayWidth * (.95 - j * .036), displayHeight * .85))

        timer()
        display_message("score: ", (20, displayHeight * .9), 40)
        display_message(str(score), (145, displayHeight * .9 + 5), 40)

        for event in pygame.event.get():

            if event == pygame.MOUSEMOTION:
                mouseOut = False
                targetMove()
            else:
                mouseOut = True

            pygame.mouse.set_visible(False)

            if event.type == pygame.QUIT:
                gameExit = True  # breaks out of the loop
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                shoot(mousePosition[0] - 25, (mousePosition[1] - 25))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                bullets = 5
                sound(reload, .1)
                message = False

            display_changing(event)

        pygame.display.update()  # updates frame
        clock.tick(200)  # sets frames per second


def game_start():
    global displayWidth
    global displayHeight
    global message
    global background
    global gameExit
    global game_time
    game_time = 60

    while not gameExit:
        menu_colors = [(200, 30, 30), (200, 30, 30)]
        screen_resize()

        gameDisplay.blit(background2, (0, 0))

        mousePosition = pygame.mouse.get_pos()
        targetMove()
        for d in range(len(menu_dimentions)):
            if menu_dimentions[d][0] < mousePosition[0] < menu_dimentions[d][0] + 200 and \
                    menu_dimentions[d][1] < mousePosition[1] < menu_dimentions[d][1] + displayHeight * .07:
                menu_colors[d] = (255, 255, 100)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                if menu_colors[0] == (255, 255, 100):
                    game_loop()
                elif menu_colors[1] == (255, 255, 100):
                    gameExit = True
                # if menu_colors[2] == (255,255,100):
                #     gameExit = True
            display_changing(event)

        if not gameExit:
            display_message('NEW GAME', menu_dimentions[0], 40, menu_colors[0])
            display_message('QUIT', menu_dimentions[1], 40, menu_colors[1])

            pygame.display.update()  # updates frame
            clock.tick(10)  # sets frames per second


score_time_limit = 4
score_time = now()


def hall_of_fame():
    global score
    global score_time_limit
    global score_time
    score_time_limit = 4
    while not gameExit:
        gameDisplay.blit(background2, (0, 0))
        birdMove()
        targetMove()
        if now() - score_time > 1:
            score_time_limit -= 1
            score_time = now()
            if score_time_limit == 0:
                game_start()
        for event in pygame.event.get():
            screen_resize()
            display_changing(event)

        if not gameExit:
            display_message('YOUR SCORE IS: ', ((displayWidth - text_width('YOUR SCORE IS: ', 40)) * .5, displayHeight * .3), 40)
            display_message(str(score), ((displayWidth - text_width(str(score), 40)) * .5, displayHeight * .4), 40)
            # display_message( 'RETURN TO MAIN MENU', ( (displayWidth - text_width( 'RETURN TO MAIN MENU',40)) *.5, displayHeight*.4 ), 40 )

            pygame.display.update()  # updates frame
            clock.tick(70)  # sets frames per second


game_start()
pygame.quit()
quit()
