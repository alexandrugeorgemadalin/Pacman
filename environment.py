import pygame

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

    def load_level(self):
        file = "level-%s.txt" % self.level_no
        self.food_count = 0
        with open(file) as f:
            for line in f:
                row = []
                for block in line.strip():
                    if block == '.' or block == '*':
                        self.food_count += 1
                    row.append(block)
                self.world.append(row)
        self.width = len(self.world[0])
        self.heigth = len(self.world)

    def draw_map(self, screen):
        for y, row in enumerate(self.world):
            for x, block in enumerate(row):
                image = self.char_to_image.get(block, None)
                if image:
                    screen.blit(pygame.image.load('./images/' + image), (x * BLOCK_SIZE, y * BLOCK_SIZE))
