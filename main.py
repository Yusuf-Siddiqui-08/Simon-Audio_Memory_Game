import pygame
import random

from pygame import SurfaceType

screenSize = (720, 720)

#colour constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

class Button:
    def __init__(self, button_type, image: str = None, rect: tuple = None, position=None, color: tuple = None):
        self.position = position
        self.image = image
        self.type = button_type
        if image is not None and button_type == "image":
            self.image = pygame.image.load(image)
            if position is None:
                raise Exception("No position parameter entered!")
            else:
                if self.position == "center":
                    self.x = (screenSize[0] / 2) - (self.image.get_width() / 2)
                    self.y = (screenSize[1] / 2) - (self.image.get_height() / 2)
                elif isinstance(position, tuple):
                    self.x = self.position[0]
                    self.y = self.position[1]
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.x, self.y)
        elif button_type == "rect":
            self.color = color
            self.rect = rect
            if self.rect is None:
                raise Exception("No rect coordinates parameter entered!")
            else:
                self.rect = pygame.Rect(self.rect)
                self.x = self.rect.topleft[0]
                self.y = self.rect.topleft[1]
        self.clicked = False

    def draw(self, surface, event_list):
        for _event in event_list:
            if _event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(_event.pos):
                    self.clicked = True
                if self.rect.collidepoint(_event.pos):
                    if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                        self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.type == "image":
            surface.blit(self.image, (self.x, self.y))
        elif self.type == "rect":
            pygame.draw.rect(screen, self.color, self.rect)

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode(screenSize)

font = pygame.font.SysFont("dubai", 100)
title = font.render("SIMON", True, WHITE)
title_rect = title.get_rect(center=(screenSize[0]/2, 200))

do_sound = pygame.mixer.Sound("music/do.mp3")
re_sound = pygame.mixer.Sound("music/re.mp3")
mi_sound = pygame.mixer.Sound("music/mi.mp3")
fa_sound = pygame.mixer.Sound("music/fa.mp3")
soundDict = {1: do_sound, 2: re_sound, 3: mi_sound, 4: fa_sound}

play_button = Button(button_type="image", image="buttons/play_button.jpg", position="center")
exit_button = Button(button_type="image", image="buttons/exit_button.png", position=((screenSize[0] / 2) - 140, play_button.y + 100))

button_h = 100
button_w = 100
spacer = 10
grid = ((screenSize[0] / 2) - 105, (screenSize[1] / 2) - 60, 210, 210)
# grid for the buttons. topleft x, topleft y, width, height
buttonPosList = [(grid[0], grid[1], button_w, button_h),
                 (grid[0], grid[1] + button_h + spacer, button_w, button_h),
                 (grid[0] + button_w + spacer, grid[1] + button_h + spacer, button_w, button_h),
                 (grid[0] + button_w + spacer, grid[1], button_w, button_h)]


# button position list in order of yellow, red, green, blue
# +--------+-------+
# | Yellow | Blue  |
# +--------+-------+
# |  Red   | Green |
# +--------+-------+

# +--------+-------+
# | 1      | 4     |
# +--------+-------+
# | 2      | 3     |
# +--------+-------+
# Table made with https://ozh.github.io/ascii-tables/


def resetGameButtons():
    global y_button, r_button, g_button, b_button, buttonDict
    y_button = Button("rect", rect=buttonPosList[0], color=YELLOW)
    r_button = Button("rect", rect=buttonPosList[1], color=RED)
    g_button = Button("rect", rect=buttonPosList[2], color=GREEN)
    b_button = Button("rect", rect=buttonPosList[3], color=BLUE)
    buttonDict = {1: y_button, 2: r_button, 3: g_button, 4: b_button}


def drawGameButtons():
    y_button.draw(screen, eventList)
    b_button.draw(screen, eventList)
    r_button.draw(screen, eventList)
    g_button.draw(screen, eventList)

def drawGameTitle(surface: SurfaceType):
    surface.blit(title, title_rect)


resetGameButtons()
sequence = []
run = True
stage = 0


# +------+--------+
# | Code | Stage  |
# +------+--------+
# |    0 | MENU   |
# |    1 | SAMPLE |
# |    2 | TEST   |
# |    3 | DEAD   |
# +------+--------+
# Table made with https://ozh.github.io/ascii-tables/

while run:
    screen.fill(BLACK)
    eventList = pygame.event.get()
    for event in eventList:
        if event.type == pygame.QUIT:
            run = False
    drawGameTitle(screen)
    if stage == 0:
        play_button.draw(screen, eventList)
        exit_button.draw(screen, eventList)
        if play_button.clicked is True:
            stage = 1
        elif exit_button.clicked is True:
            run = False
    elif stage == 1:
        sequence.append(random.randint(1, 4))
        for num in sequence:
            resetGameButtons()
            screen.fill(BLACK)
            drawGameTitle(screen)
            if num == 1:
                y_button.color = WHITE
            elif num == 2:
                r_button.color = WHITE
            elif num == 3:
                g_button.color = WHITE
            elif num == 4:
                b_button.color = WHITE
            drawGameButtons()
            pygame.display.flip()
            pygame.mixer.Sound.play(soundDict[num])
            pygame.time.delay(2500)
        stage = 2
        part = 0
    elif stage == 2:
        resetGameButtons()
        drawGameButtons()
        button_clicked = None
        if y_button.clicked:
            button_clicked = 1
        elif r_button.clicked:
            button_clicked = 2
        elif g_button.clicked:
            button_clicked = 3
        elif b_button.clicked:
            button_clicked = 4
        if button_clicked is not None:
            pygame.mixer.Sound.play(soundDict[button_clicked])
            if sequence[part] == button_clicked:
                part += 1
                if part >= len(sequence):
                    stage = 1
            else:
                stage = 3
    elif stage == 3:
        run = False

    pygame.display.flip()
