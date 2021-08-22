import pygame


class Menu:
    pygame.init()

    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    smallfont = pygame.font.Font('freesansbold.ttf', 22)

    button_width = 140
    button_height = 40
    button1 = smallfont.render('Manual', True, (255, 255, 255))
    button2 = smallfont.render('Auto', True, (255, 255, 255))
    button1X, button1Y = 83, 310
    button2X, button2Y = 374, 310

    titleFont = pygame.font.Font('freesansbold.ttf', 40)
    titleX = 125
    titleY = 100
    title = titleFont.render('Pacman Game', True, (255, 255, 255))

    messageFont = pygame.font.Font('freesansbold.ttf', 24)
    messageX = 160
    messageY = 150
    message = messageFont.render('Select game mode', True, (255, 255, 255))

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def update_screen(self, screen):
        screen.blit(self.button1, (self.button1X, self.button1Y))
        screen.blit(self.button2, (self.button2X, self.button2Y))
        screen.blit(self.title, (self.titleX, self.titleY))
        screen.blit(self.message, (self.messageX, self.messageY))

    def create_menu(self):
        screen = pygame.display.set_mode((self.width, self.height))

        running = True
        mode = None
        while running:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button1X <= mouse[0] <= self.button1X + self.button_width and \
                            self.button1Y <= mouse[1] <= self.button1Y + self.button_height:
                        mode = 'MANUAL'
                        running = False
                    elif self.button2X <= mouse[0] <= self.button2X + self.button_width and \
                            self.button2Y <= mouse[1] <= self.button2Y + self.button_height:
                        mode = 'AUTO'
                        running = False
            screen.fill((60, 25, 60))
            if self.button1X <= mouse[0] <= self.button1X + self.button_width and \
                    self.button1Y <= mouse[1] <= self.button1Y + self.button_height:
                pygame.draw.rect(screen, self.color_light, [50, 300, 140, 40])
            else:
                pygame.draw.rect(screen, self.color_dark, [50, 300, 140, 40])
            if self.button2X <= mouse[0] <= self.button2X + self.button_width and \
                    self.button2Y <= mouse[1] <= self.button2Y + self.button_height:
                pygame.draw.rect(screen, self.color_light,
                                 [self.width - 190, 300, self.button_width, self.button_height])
            else:
                pygame.draw.rect(screen, self.color_dark,
                                 [self.width - 190, 300, self.button_width, self.button_height])
            self.update_screen(screen)
            pygame.display.update()
        return mode
