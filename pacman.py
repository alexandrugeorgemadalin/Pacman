import pygame

BLOCK_SIZE = 32


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
        self.score = 0
        self.radius = 5 * BLOCK_SIZE

    def update_image_state(self, state):
        self.image = pygame.image.load(self.state_to_image[state])

    def check_radius(self, x, y, ghost):
        if x - self.radius <= ghost.x <= x + self.radius and \
                y - self.radius <= ghost.y <= y + self.radius:
            return True
        return False

    def check_ghosts(self, environment):
        for ghost in environment.ghosts:
            if ghost.eatable is True and self.x == ghost.x and self.y == ghost.y:
                self.score += 20
                environment.ghosts.remove(ghost)

    def detect_collision(self, x, y, environment, rewards):
        # detect collision with walls
        if environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)] == '=':
            return True
        elif environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)] in rewards:
            if environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)] == '*':
                for ghost in environment.ghosts:
                    if self.check_radius(x, y, ghost):
                        ghost.eatable = True
            self.score += rewards[environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)]]
            environment.food_count -= 1
            environment.world[int(x / BLOCK_SIZE)][int(y / BLOCK_SIZE)] = ' '
            return False
        else:
            return False

    def draw_pacman(self, screen):
        screen.blit(self.image, (self.y, self.x))

    def move_right(self, dy, environment, rewards):
        new_Y = self.y + dy
        if int(new_Y / BLOCK_SIZE) > environment.width:
            pass
        elif not self.detect_collision(self.x, new_Y, environment, rewards):
            self.update_image_state('right')
            self.y += dy
            self.check_ghosts(environment)

    def move_left(self, dy, environment, rewards):
        new_Y = self.y - dy
        if int(new_Y / BLOCK_SIZE) < 0:
            pass
        elif not self.detect_collision(self.x, new_Y, environment, rewards):
            self.update_image_state('left')
            self.y -= dy
            self.check_ghosts(environment)

    def move_down(self, dx, environment, rewards):
        new_X = self.x + dx
        if int(new_X / BLOCK_SIZE) > environment.heigth:
            pass
        elif not self.detect_collision(new_X, self.y, environment, rewards):
            self.update_image_state('down')
            self.x += dx
            self.check_ghosts(environment)

    def move_up(self, dx, environment, rewards):
        new_X = self.x - dx
        if int(new_X / BLOCK_SIZE) < 0:
            pass
        elif not self.detect_collision(new_X, self.y, environment, rewards):
            self.update_image_state('up')
            self.x -= dx
            self.check_ghosts(environment)
