import pygame


class Checkbox:
    def __init__(self, surface, x, y, idnum, caption, color=(255, 255, 255), outline_color=(25, 25, 25),
                 check_color=(0, 0, 0), font_size=22, font_color=(255, 255, 255), text_offset=(28, 1),
                 font='Ariel Black'):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font

        # identification for removal and reorginazation
        self.idnum = idnum

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def draw_button_text(self):
        self.font = pygame.font.Font('freesansbold.ttf', 21)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 + self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.oc, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self.draw_button_text()

    def _update(self, event_object):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)


class Menu:
    pygame.init()

    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    smallfont = pygame.font.Font('freesansbold.ttf', 22)

    button_width = 140
    button_height = 40
    button1 = smallfont.render('Manual', True, (255, 255, 255))
    button2 = smallfont.render('Auto', True, (255, 255, 255))
    button1X, button1Y = 83, 360
    button2X, button2Y = 374, 360

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

    def update_screen(self, screen, boxes):
        screen.blit(self.button1, (self.button1X, self.button1Y))
        screen.blit(self.button2, (self.button2X, self.button2Y))
        screen.blit(self.title, (self.titleX, self.titleY))
        screen.blit(self.message, (self.messageX, self.messageY))
        for box in boxes:
            box.render_checkbox()

    def create_menu(self):
        screen = pygame.display.set_mode((self.width, self.height))

        boxes = []
        box1 = Checkbox(screen, 200, 200, 1, 'level-1')
        box2 = Checkbox(screen, 200, 250, 2, 'level-2')
        box3 = Checkbox(screen, 200, 300, 3, 'level-3')
        boxes.append(box1)
        boxes.append(box2)
        boxes.append(box3)

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for box in boxes:
                        box.update_checkbox(event)
                        if box.checked is True:
                            for b in boxes:
                                if b != box:
                                    b.checked = False
            screen.fill((95, 158, 160))
            if self.button1X <= mouse[0] <= self.button1X + self.button_width and \
                    self.button1Y <= mouse[1] <= self.button1Y + self.button_height:
                pygame.draw.rect(screen, self.color_light, [50, 350, 140, 40])
            else:
                pygame.draw.rect(screen, self.color_dark, [50, 350, 140, 40])
            if self.button2X <= mouse[0] <= self.button2X + self.button_width and \
                    self.button2Y <= mouse[1] <= self.button2Y + self.button_height:
                pygame.draw.rect(screen, self.color_light,
                                 [self.width - 190, 350, self.button_width, self.button_height])
            else:
                pygame.draw.rect(screen, self.color_dark,
                                 [self.width - 190, 350, self.button_width, self.button_height])
            self.update_screen(screen, boxes)
            pygame.display.update()
        for box in boxes:
            if box.checked:
                return mode, box.idnum
