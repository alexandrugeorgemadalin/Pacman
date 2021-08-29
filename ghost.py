import pygame
import random

BLOCK_SIZE = 32

directions = ['left', 'right', 'up', 'down']


class Ghost:
    ghosts_types = {
        'g': './images/ghost1.png',
        'G': './images/ghost2.png'
    }

    def __init__(self, x, y, type):
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE
        self.type = type
        self.image = pygame.image.load(self.ghosts_types.get(self.type, None))
        self.direction = None

    # x, y inversed
    def draw_ghost(self, screen):
        screen.blit(self.image, (self.y, self.x))

    def detect_wall_collision(self, x, y, environment):
        if environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)] == '=':
            return True
        else:
            return False

    def move_ghost(self, environment):
        if self.direction is None:
            self.direction = random.choice(directions)
        if self.direction == 'left':
            new_Y = self.y - BLOCK_SIZE
            if int(new_Y / BLOCK_SIZE) < 0:
                pass
            elif not self.detect_wall_collision(self.x, new_Y, environment):
                self.y = new_Y
            else:
                self.direction = None
        elif self.direction == 'right':
            new_Y = self.y + BLOCK_SIZE
            if int(new_Y / BLOCK_SIZE) > environment.width:
                pass
            elif not self.detect_wall_collision(self.x, new_Y, environment):
                self.y = new_Y
            else:
                self.direction = None
        elif self.direction == 'up':
            new_X = self.x - BLOCK_SIZE
            if int(new_X / BLOCK_SIZE) < 0:
                pass
            elif not self.detect_wall_collision(new_X, self.y, environment):
                self.x = new_X
            else:
                self.direction = None
        elif self.direction == 'down':
            new_X = self.x + BLOCK_SIZE
            if int(new_X / BLOCK_SIZE) > environment.heigth:
                pass
            elif not self.detect_wall_collision(new_X, self.y, environment):
                self.x = new_X
            else:
                self.direction = None
