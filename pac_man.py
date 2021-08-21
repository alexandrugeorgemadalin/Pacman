import pygame
import random

TITLE = 'Pac-Man'
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
        with open(file) as f:
            for line in f:
                row = []
                for block in line.strip():
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


rewards = {
    '*': 10,
    '.': 1
}


def show_score(x, y, pacman_score):
    score = scoreFont.render("Score: " + str(pacman_score), True, (255, 255, 255))
    screen.blit(score, (x, y))


class Pacman:
    state_to_image = {
        'up': './images/pacman_up.png',
        'down': './images/pacman_down.png',
        'right': './images/pacman_right.png',
        'left': './images/pacman_left.png'
    }

    def __init__(self, x, y, state):
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE
        self.update_image_state(state)
        # self.image = pygame.image.load(self.state_to_image[state])
        self.score = 0

    def update_image_state(self, state):
        self.image = pygame.image.load(self.state_to_image[state])

    def detect_collision(self, x, y, environment):
        # detect collision with walls
        if environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)] == '=':
            return True
        elif environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)] in rewards:
            self.score += rewards[environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)]]
            environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)] = ' '
            return False
        else:
            return False

    def draw_pacman(self, screen):
        screen.blit(self.image, (self.y, self.x))

    def move_right(self, dy, environment):
        new_Y = self.y + dy
        if int(new_Y / BLOCK_SIZE) > environment.width:
            pass
        elif not self.detect_collision(self.x, new_Y, environment):
            self.update_image_state('right')
            self.y += dy

    def move_left(self, dy):
        new_Y = self.y - dy
        if int(new_Y / BLOCK_SIZE) < 0:
            pass
        elif not self.detect_collision(self.x, new_Y, environment):
            self.update_image_state('left')
            self.y -= dy

    def move_down(self, dx):
        new_X = self.x + dx
        if int(new_X / BLOCK_SIZE) > environment.heigth:
            pass
        elif not self.detect_collision(new_X, self.y, environment):
            self.update_image_state('down')
            self.x += dx

    def move_up(self, dx):
        new_X = self.x - dx
        if int(new_X / BLOCK_SIZE) < 0:
            pass
        elif not self.detect_collision(new_X, self.y, environment):
            self.update_image_state('up')
            self.x -= dx


def update_screen(screen):
    screen.fill((0, 0, 0))
    environment.draw_map(screen)
    pacman.draw_pacman(screen)
    show_score(scoreX, scoreY, pacman.score)


if __name__ == '__main__':
    # Create the environment
    environment = Environment(1)
    # Load the environment level
    environment.load_level()

    pacman = Pacman(1, 1, 'right')

    # Initialize the game
    pygame.init()

    # Create the game screen
    screen = pygame.display.set_mode((environment.width * BLOCK_SIZE, environment.heigth * BLOCK_SIZE))

    # Draw the maze
    environment.draw_map(screen)
    pacman.draw_pacman(screen)

    scoreFont = pygame.font.Font('freesansbold.ttf', 23)
    scoreX = 6
    scoreY = 6

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pacman.move_right(BLOCK_SIZE, environment)
                if event.key == pygame.K_LEFT:
                    pacman.move_left(BLOCK_SIZE)
                if event.key == pygame.K_UP:
                    pacman.move_up(BLOCK_SIZE)
                if event.key == pygame.K_DOWN:
                    pacman.move_down(BLOCK_SIZE)
        update_screen(screen)
        pygame.display.update()
