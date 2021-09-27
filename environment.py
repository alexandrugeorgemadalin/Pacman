import pygame
from ghost import Ghost

BLOCK_SIZE = 32


class Environment:
    world = []
    char_to_image = {
        '.': 'dot.png',
        '=': 'wall.png',
        '*': 'power.png'
    }

    def __init__(self, level_no, ):
        self.level_no = level_no

    # function that load the map from the level.txt file
    def load_level(self):
        file = "level-%s.txt" % self.level_no
        self.food_count = 0
        self.ghosts = []
        with open(file) as f:
            i = 0
            for line in f:
                row = []
                j = 0
                for block in line.strip():
                    if block == '.' or block == '*':
                        self.food_count += 1
                    if block == 'g' or block == 'G':
                        self.ghosts.append(Ghost(i, j, block))
                        block = ' '
                    row.append(block)
                    j += 1
                self.world.append(row)
                i += 1
        self.width = len(self.world[0])
        self.heigth = len(self.world)

    # function that draw the map on the game screen
    def draw_map(self, screen):
        for y, row in enumerate(self.world):
            for x, block in enumerate(row):
                image = self.char_to_image.get(block, None)
                if image:
                    screen.blit(pygame.image.load('./images/' + image), (x * BLOCK_SIZE, y * BLOCK_SIZE))
