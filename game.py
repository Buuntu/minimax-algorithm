from copy import deepcopy
from random import randint

class Game:
    'Class used to keep track of the board and calculate computer moves'

    def __init__(self, player='X', computer='O'):
        self.player = player
        self.computer = computer
        self.empty = ' '

        self.board = [[self.empty for x in range(3)] for x in range(3)]

    # Calculate computer move based on minimax algorithm
    def calculate_move(self):
        # if it's the computer's first turn, take one of the corners (much faster than calculating with recursion)
        if self.is_board_empty():
            move = self.random_corner()
            return {'row': move[0], 'col': move[1]}

        move = self.minimax(self.computer, [-2, None], [2, None])

        if not move[1]:
            # Game is over
            return False
        else:
            return {'row': move[1][0], 'col': move[1][1]}

    # minimax algorithm (using alpha beta pruning to speed up) to calculate the best move for the computer
    # assigning 1 for player win, 0 for draw, and -1 for computer win
    def minimax(self, mark, alpha, beta):
        # Check if the game is over and return assigned value if it is
        if self.has_won(self.player):
            return [1, None]
        elif self.has_won(self.computer):
            return [-1, None]
        elif self.tied():
            return [0, None]

        # If it's the player's turn
        if mark == self.player:
            # Loop through available moves
            for move in self.get_moves():
                new_board = Game(self.player, self.computer)
                new_board.board = deepcopy(self.board)
                alpha_copy = deepcopy(alpha)
                beta_copy = deepcopy(beta)

                # Recursive call to get value for each node
                value = new_board.move(mark, move[0], move[1]).minimax(self.opponent(mark), alpha_copy, beta_copy)[0]

                # if next move is max
                if value > alpha[0]:
                    alpha = [value, move]

                # "prune" branches
                if alpha[0] >= beta[0]:
                    return alpha

            return alpha
        else:
            for move in self.get_moves():
                new_board = Game(self.player, self.computer)
                new_board.board = deepcopy(self.board)
                alpha_copy = deepcopy(alpha)
                beta_copy = deepcopy(beta)

                # Recursive call
                value = new_board.move(mark, move[0], move[1]).minimax(self.opponent(mark), alpha_copy, beta_copy)[0]

                # if next move is min
                if value < beta[0]:
                    beta = [value, move]

                # alpha beta pruning
                if beta[0] <= alpha[0]:
                    return beta

            return beta

    # Get the "opposite" mark
    def opponent(self, mark):
        if mark == self.player:
            return self.computer
        else:
            return self.player

    # Gets a list of available moves
    def get_moves(self):
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == self.empty:
                    moves.append([r, c])

        return moves

    # Checks if the game is tied
    def tied(self):
        if not self.has_won(self.player) and not self.has_won(self.computer) and self.is_board_full():
            return True

        return False

    # Checks if there are moves left
    def is_board_full(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == self.empty:
                    return False

        return True

    # Checks if it's a new game
    def is_board_empty(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] != self.empty:
                    return False

        return True

    # Returns the winning list of coordinates as a list or false otherwise
    def has_won(self, mark):
        has_won_horizontal = self.won_horizontal(mark)
        if has_won_horizontal:
            return has_won_horizontal

        has_won_vertical = self.won_vertical(mark)
        if has_won_vertical:
            return has_won_vertical

        has_won_diagonal = self.won_diagonal(mark)
        if has_won_diagonal:
            return has_won_diagonal

        return False

    # Returns the winning vertical combination as a list of coordinates or false
    def won_vertical(self, mark):
        for col in range(3):
            if self.board[0][col] == mark and self.board[0][col] == self.board[1][col] == self.board[2][col]:
                return [[0, col], [1, col], [2, col]]

        return False

    # Returns the winning horizontal combination as a list of coordinates or false
    def won_horizontal(self, mark):
        for row in range(3):
            if self.board[row][0] == mark and self.board[row][0] == self.board[row][1] == self.board[row][2]:
                return [[row, 0], [row, 1], [row, 2]]

        return False

    # Returns the winning diagonal combination as a list of coordinates or false
    def won_diagonal(self, mark):
        if self.board[0][0] == mark and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return [[0, 0], [1, 1], [2, 2]]
        elif self.board[2][0] == mark and self.board[2][0] == self.board[1][1] == self.board[0][2]:
            return [[2, 0], [1, 1], [0, 2]]

    def make_player_move(self, row, col):
        return self.move(self.player, row, col)

    def make_computer_move(self, row, col):
        return self.move(self.computer, row, col)

    def move(self, mark, row, col):
        if self.board[row][col] == self.empty:
            self.board[row][col] = mark

        return self

    # Pick a random corner
    def random_corner(self):
        i = randint(1, 4)
        if i == 1:
            return [0, 0]
        elif i == 2:
            return [2, 0]
        elif i == 3:
            return [0, 2]
        else:
            return [2, 2]
