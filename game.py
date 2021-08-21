import pygame
import random
from environment import Environment
from pacman import Pacman

TITLE = 'Pac-Man'
BLOCK_SIZE = 32

rewards = {
    '*': 10,
    '.': 1
}


def show_score(x, y, pacman_score):
    score = scoreFont.render("Score: " + str(pacman_score), True, (255, 255, 255))
    screen.blit(score, (x, y))


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
                    pacman.move_right(BLOCK_SIZE, environment, rewards)
                if event.key == pygame.K_LEFT:
                    pacman.move_left(BLOCK_SIZE, environment, rewards)
                if event.key == pygame.K_UP:
                    pacman.move_up(BLOCK_SIZE, environment, rewards)
                if event.key == pygame.K_DOWN:
                    pacman.move_down(BLOCK_SIZE, environment, rewards)
        update_screen(screen)
        pygame.display.update()
