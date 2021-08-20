import pygame

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


class Pacman:
    def __init__(self, x, y):
        self.x = x * BLOCK_SIZE
        self.y = y * BLOCK_SIZE
        self.image = pygame.image.load('./images/pacman_o.png')

    def detect_collision(self, x, y, environment):
        # detect collision with walls
        if environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)] == '=':
            return True
        else:
            return False

    def draw_pacman(self, screen):
        screen.blit(self.image, (self.y, self.x))

    def move_right(self, y, environment):
        new_Y = self.y + y
        if int(new_Y / BLOCK_SIZE) > environment.width:
            pass
        elif not self.detect_collision(self.x, new_Y, environment):
            self.y += y

    def move_left(self, y):
        new_Y = self.y - y
        if int(new_Y / BLOCK_SIZE) < 0:
            pass
        elif not self.detect_collision(self.x, new_Y, environment):
            self.y -= y

    def move_down(self, x):
        new_X = self.x + x
        if int(new_X / BLOCK_SIZE) > environment.heigth:
            pass
        elif not self.detect_collision(new_X, self.y, environment):
            self.x += x

    def move_up(self, x):
        new_X = self.x - x
        if int(new_X / BLOCK_SIZE) < 0:
            pass
        elif not self.detect_collision(new_X, self.y, environment):
            self.x -= x


def update_screen(screen):
    screen.fill((0, 0, 0))
    environment.draw_map(screen)
    pacman.draw_pacman(screen)


if __name__ == '__main__':
    # Create the environment
    environment = Environment(1)
    # Load the environment level
    environment.load_level()

    pacman = Pacman(1, 2)

    # Initialize the game
    pygame.init()

    # Create the game screen
    screen = pygame.display.set_mode((environment.width * BLOCK_SIZE, environment.heigth * BLOCK_SIZE))

    # Draw the maze
    environment.draw_map(screen)
    pacman.draw_pacman(screen)

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
