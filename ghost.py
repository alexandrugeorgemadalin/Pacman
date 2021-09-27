import pygame
import random

BLOCK_SIZE = 32

directions = ['left', 'right', 'up', 'down']


# function that detect collision with walls
def detect_wall_collision(x, y, environment):
    if environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)] == '=':
        return True
    else:
        return False


class Ghost:
    ghosts_types = {
        'g': './images/ghost1.png',
        'G': './images/ghost2.png',
        'E': './images/ghost_white.png'
    }

    def __init__(self, x, y, type):
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE
        self.type = type
        self.image = pygame.image.load(self.ghosts_types.get(self.type, None))
        self.direction = None
        self.eatable = False

    # x, y inversed because of the pygame grid
    def draw_ghost(self, screen):
        if self.eatable:
            self.image = pygame.image.load(self.ghosts_types.get('E', None))
        screen.blit(self.image, (self.y, self.x))

    # function that move a ghost using its direction
    # a ghost keeps its direction until a wall collision is detected
    def move_ghost(self, environment):
        # if the direction is set to None a random direction is generated
        if self.direction is None:
            self.direction = random.choice(directions)
        if self.direction == 'left':
            new_Y = self.y - BLOCK_SIZE
            if int(new_Y / BLOCK_SIZE) < 0:
                pass
            elif not detect_wall_collision(self.x, new_Y, environment):
                self.y = new_Y
            else:
                self.direction = None
        elif self.direction == 'right':
            new_Y = self.y + BLOCK_SIZE
            if int(new_Y / BLOCK_SIZE) > environment.width:
                pass
            elif not detect_wall_collision(self.x, new_Y, environment):
                self.y = new_Y
            else:
                self.direction = None
        elif self.direction == 'up':
            new_X = self.x - BLOCK_SIZE
            if int(new_X / BLOCK_SIZE) < 0:
                pass
            elif not detect_wall_collision(new_X, self.y, environment):
                self.x = new_X
            else:
                self.direction = None
        elif self.direction == 'down':
            new_X = self.x + BLOCK_SIZE
            if int(new_X / BLOCK_SIZE) > environment.heigth:
                pass
            elif not detect_wall_collision(new_X, self.y, environment):
                self.x = new_X
            else:
                self.direction = None
