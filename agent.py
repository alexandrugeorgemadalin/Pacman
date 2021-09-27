import numpy as np


def path_to_moves(shortest_path):
    moves = []
    for i in range(1, len(shortest_path)):
        if shortest_path[i - 1][1] == shortest_path[i][1] and shortest_path[i - 1][0] - shortest_path[i][0] == 1:
            moves.append('up')
        elif shortest_path[i - 1][1] == shortest_path[i][1] and shortest_path[i - 1][0] - shortest_path[i][0] == -1:
            moves.append('down')
        elif shortest_path[i - 1][0] == shortest_path[i][0] and shortest_path[i - 1][1] - shortest_path[i][1] == 1:
            moves.append('left')
        elif shortest_path[i - 1][0] == shortest_path[i][0] and shortest_path[i - 1][1] - shortest_path[i][1] == -1:
            moves.append('right')
    return moves


class PacmanAgent:
    # define actions
    # numeric action codes: 0 = up, 1 = right, 2 = down, 3 = left
    actions = ['up', 'right', 'down', 'left']

    def __init__(self, rows, columns, environment):
        self.rows = rows
        self.columns = columns
        self.environment = environment
        # Create a 3D numpy array to hold the current Q-values for each state and action
        # pair: Q(s,a)
        # The array contains a number of rows and columns, as well as a third "action"
        # dimension. The action dimension consists of 4 layers that will allow us to
        # keep track of the Q-values for each posible action in each state
        self.q_values = np.zeros((self.rows, self.columns, 4))
        self.rewards = None

    def set_rewards(self, endx, endy):
        # define the map, set the path where the pacman can walk with -1
        # and the walls with -100
        self.rewards = np.full((self.rows, self.columns), 0)
        for x, row in enumerate(self.environment.world):
            for y, block in enumerate(row):
                if block == '=':
                    self.rewards[x][y] = -100
                elif block == ' ' or block == '.' or block == '*':
                    self.rewards[x][y] = -1
        self.rewards[endx][endy] = 100

    # define a function that determines if the specified location is a terminal state
    def is_terminal_state(self, current_row_index, current_column_index):
        # if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'black square')
        if self.rewards[current_row_index, current_column_index] == 100:
            return True
        else:
            return False

    # define a function that will chose a random, non-terminal starting location
    def get_starting_location(self):
        # get a random row and column index
        current_row_index = np.random.randint(self.rows)
        current_column_index = np.random.randint(self.columns)
        # continue choosing random row and column indexes until a non-terminal state is identified
        # (i.e., until the chosen state is a 'white square').
        while self.is_terminal_state(current_row_index, current_column_index):
            current_row_index = np.random.randint(self.rows)
            current_column_index = np.random.randint(self.columns)
        return current_row_index, current_column_index

    # define an epsilon greedy algorithm that will choose which action to take next
    def get_next_action(self, current_row_index, current_column_index, epsilon):
        # if a randomly chosen value between 0 and 1 is less than epsilon,
        # then choose the most promising value from the Q-table for this state.
        if np.random.random() < epsilon:
            return np.argmax(self.q_values[current_row_index, current_column_index])
        else:  # choose a random action
            return np.random.randint(4)

    # define a function that will get the next location based on the chosen action
    def get_next_location(self, current_row_index, current_column_index, action_index):
        new_row_index = current_row_index
        new_column_index = current_column_index
        if self.actions[action_index] == 'up' and current_row_index > 0:
            new_row_index -= 1
        elif self.actions[action_index] == 'right' and current_column_index < self.columns - 1:
            new_column_index += 1
        elif self.actions[action_index] == 'down' and current_row_index < self.rows - 1:
            new_row_index += 1
        elif self.actions[action_index] == 'left' and current_column_index > 0:
            new_column_index -= 1
        return new_row_index, new_column_index

    # define a function that will get the shortest path between any location
    def get_shortest_path(self, start_row_index, start_column_index):
        # return immediately if this is an invalid starting location
        if self.is_terminal_state(start_row_index, start_column_index):
            return []
        else:  # if this is a 'legal' starting location
            current_row_index, current_column_index = start_row_index, start_column_index
            shortest_path = [[current_row_index, current_column_index]]
            # continue moving along the path until we reach the goal
            while not self.is_terminal_state(current_row_index, current_column_index):
                # get the best action to take
                action_index = self.get_next_action(current_row_index, current_column_index, 1.)
                # move to the next location on the path, and add the new location to the list
                current_row_index, current_column_index = self.get_next_location(current_row_index,
                                                                                 current_column_index,
                                                                                 action_index)
                shortest_path.append([current_row_index, current_column_index])
            return shortest_path

    # define training parameters
    # epsilon - the percentage of time when we should take the best action
    # discount_factor - discount factor for future rewards
    # learning_rate - the rate at which the AI agent should learn
    def train_agent(self, epsilon, discount_factor, learning_rate, epochs_no):
        for epoch in range(epochs_no):
            # get the starting location for this episode
            row_index, column_index = self.get_starting_location()

            # continue taking actions (i.e., moving) until we reach a terminal state
            # (i.e., until we reach the item packaging area or crash into an item storage location)
            while not self.is_terminal_state(row_index, column_index):
                # choose which action to take (i.e., where to move next)
                action_index = self.get_next_action(row_index, column_index, epsilon)

                # perform the chosen action, and transition to the next state (i.e., move to the next location)
                old_row_index, old_column_index = row_index, column_index  # store the old row and column indexes
                row_index, column_index = self.get_next_location(row_index, column_index, action_index)

                # receive the reward for moving to the new state, and calculate the temporal difference
                reward = self.rewards[row_index, column_index]
                old_q_value = self.q_values[old_row_index, old_column_index, action_index]
                temporal_difference = reward + (
                        discount_factor * np.max(self.q_values[row_index, column_index])) - old_q_value

                # update the Q-value for the previous state and action pair
                new_q_value = old_q_value + (learning_rate * temporal_difference)
                self.q_values[old_row_index, old_column_index, action_index] = new_q_value

        print('Training complete!')
