import pygame
import random
from environment import Environment
from pacman import Pacman
from menu import Menu
from agent import PacmanAgent

TITLE = 'Pac-Man'
BLOCK_SIZE = 32

rewards = {
    '*': 10,
    '.': 1
}

endPositions = {
    1: (6, 18),
    2: (14, 21),
    3: (21, 11)
}


def show_score(x, y, pacman_score):
    score = scoreFont.render("Score: " + str(pacman_score), True, (255, 255, 255))
    screen.blit(score, (x, y))


def update_screen(screen):
    screen.fill((0, 0, 0))
    environment.draw_map(screen)
    pacman.draw_pacman(screen)
    show_score(scoreX, scoreY, pacman.score)


def end_window():
    running = True
    end_screen = pygame.display.set_mode((400, 150))
    messageFont = pygame.font.Font('freesansbold.ttf', 30)
    messageX = 100
    messageY = 50
    message = messageFont.render('End Game!', True, (255, 255, 255))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        end_screen.fill((0, 0, 0))
        end_screen.blit(message, (messageX, messageY))
        pygame.display.update()


if __name__ == '__main__':

    # --------Selecting the game mode----------------
    running = False

    menu = Menu(520, 520)
    game_mode, level_no = menu.create_menu()

    # Create the environment
    environment = Environment(level_no)
    # Load the environment level
    environment.load_level()

    pacman = Pacman(1, 1, 'right')

    # Initialize the game
    pygame.init()

    if game_mode == 'MANUAL':

        # Create the game screen
        screen = pygame.display.set_mode((environment.width * BLOCK_SIZE, environment.heigth * BLOCK_SIZE))

        # Draw the maze

        environment.draw_map(screen)
        pacman.draw_pacman(screen)

        running = True
        scoreFont = pygame.font.Font('freesansbold.ttf', 23)
        scoreX = 6
        scoreY = 6

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
            if environment.food_count == 0:
                running = False
                pygame.time.wait(750)

        end_window()

    elif game_mode == 'AUTO':
        # define training parameters
        epsilon = 0.9  # the percentage of time when we should take the best action
        discount_factor = 0.9  # discount factor for future rewards
        learning_rate = 0.9  # the rate at which the AI agent should learn

        agent = PacmanAgent(environment.heigth, environment.width, environment)
        endX, endY = endPositions[level_no]
        agent.set_rewards(endX, endY)
        agent.train_agent(epsilon, discount_factor, learning_rate, 1000)
        shortest_path = agent.get_shortest_path(int(pacman.x / BLOCK_SIZE), int(pacman.y / BLOCK_SIZE))
        moves = agent.path_to_moves(shortest_path)

        # Create the game screen
        screen = pygame.display.set_mode((environment.width * BLOCK_SIZE, environment.heigth * BLOCK_SIZE))

        # Draw the maze

        environment.draw_map(screen)
        pacman.draw_pacman(screen)

        running = True

        scoreFont = pygame.font.Font('freesansbold.ttf', 23)
        scoreX = 6
        scoreY = 6
        move_index = 0
        while running and move_index < len(moves):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if moves[move_index] == 'up':
                pacman.move_up(BLOCK_SIZE, environment, rewards)
            elif moves[move_index] == 'down':
                pacman.move_down(BLOCK_SIZE, environment, rewards)
            elif moves[move_index] == 'right':
                pacman.move_right(BLOCK_SIZE, environment, rewards)
            elif moves[move_index] == 'left':
                pacman.move_left(BLOCK_SIZE, environment, rewards)
            pygame.time.wait(500)
            move_index += 1
            update_screen(screen)
            # set the finish block to a different wall color
            screen.blit(pygame.image.load('./images/end_wall.png'), (endY * BLOCK_SIZE, endX * BLOCK_SIZE))
            pygame.display.update()

        end_window()
