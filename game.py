import pygame
from environment import Environment
from pacman import Pacman
from menu import Menu
from agent import PacmanAgent, path_to_moves

BLOCK_SIZE = 32

# rewards for eating a point or a ball
rewards = {
    '*': 10,
    '.': 1
}

# end positions for each level when the 'AUTO' game mode is selected
endPositions = {
    1: (6, 18),
    2: (14, 21),
    3: (21, 11)
}


# function that shows the score on the screen
def show_score(x, y, pacman_score):
    score = scoreFont.render("Score: " + str(pacman_score), True, (255, 255, 255))
    screen.blit(score, (x, y))


# function that updates the screen
def update_screen(screen):
    screen.fill((0, 0, 0))
    environment.draw_map(screen)
    for ghost in environment.ghosts:
        ghost.draw_ghost(screen)
    pacman.draw_pacman(screen)
    show_score(scoreX, scoreY, pacman.score)


# function that creates the final screen at the end of the game
# displays a 'congratulations' or 'game over' message with the final score
def end_window(end_message):
    width, height = 450, 200
    running = True
    end_screen = pygame.display.set_mode((450, 200))
    messageFont = pygame.font.Font('freesansbold.ttf', 30)
    message = messageFont.render(end_message, True, (240, 255, 255))
    message2Font = pygame.font.Font('freesansbold.ttf', 20)
    message2 = message2Font.render('Final score: ' + str(pacman.score), True, (40, 40, 40))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        end_screen.fill((95, 158, 160))
        end_screen.blit(message, message.get_rect(center=(width / 2, height / 2)))
        end_screen.blit(message2, message2.get_rect(center=(width / 2, (height / 2) + 50)))
        pygame.display.update()


# function that checks if the pacman is killed by a ghost
def game_over(pacman, ghosts):
    for ghost in ghosts:
        if ghost.eatable is False and pacman.x == ghost.x and pacman.y == ghost.y:
            return True
    return False


if __name__ == '__main__':

    # Selecting the game mode and level
    menu = Menu(520, 520)
    game_mode, level_no = menu.create_menu()

    # Create the environment
    environment = Environment(level_no)
    # Load the environment level
    environment.load_level()

    pacman = Pacman(1, 1, 'right')

    # Initialize the game
    pygame.init()

    # 'MANUAL' game mode
    # the player control the pacman using arrows
    if game_mode == 'MANUAL':

        # Create the game screen
        screen = pygame.display.set_mode((environment.width * BLOCK_SIZE, environment.heigth * BLOCK_SIZE))

        # Draw the maze

        environment.draw_map(screen)
        pacman.draw_pacman(screen)
        for ghost in environment.ghosts:
            ghost.draw_ghost(screen)

        running = True
        scoreFont = pygame.font.Font('freesansbold.ttf', 23)
        scoreX = 6
        scoreY = 6
        GHOSTMOVE, t = pygame.USEREVENT + 1, 275
        pygame.time.set_timer(GHOSTMOVE, t)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # check the pressed keys to move the pacman
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        pacman.move_right(BLOCK_SIZE, environment, rewards)
                    if event.key == pygame.K_LEFT:
                        pacman.move_left(BLOCK_SIZE, environment, rewards)
                    if event.key == pygame.K_UP:
                        pacman.move_up(BLOCK_SIZE, environment, rewards)
                    if event.key == pygame.K_DOWN:
                        pacman.move_down(BLOCK_SIZE, environment, rewards)
                # after a period of t = 275 ms all ghosts move
                if event.type == GHOSTMOVE:
                    for ghost in environment.ghosts:
                        ghost.move_ghost(environment)
            update_screen(screen)
            pygame.display.update()
            # check the food count
            if environment.food_count == 0:
                running = False
                pygame.time.wait(750)
                end_window("Congratulations!")
            elif game_over(pacman, environment.ghosts):
                running = False
                pygame.time.wait(750)
                end_window("Game Over!")
    # 'AUTO' game mode
    # using a Q-learning algorithm the map is learned and is calculated the path to the end position
    # using the values calculated in the Q_value matrix
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
        moves = path_to_moves(shortest_path)

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
        GHOSTMOVE, t = pygame.USEREVENT + 1, 500
        pygame.time.set_timer(GHOSTMOVE, t)
        while running and move_index < len(moves):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # after a period of t = 500 ms all ghosts move
                if event.type == GHOSTMOVE:
                    for ghost in environment.ghosts:
                        ghost.move_ghost(environment)
            # check what move is next
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

        end_window("Congratulations!")
