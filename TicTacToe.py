import random
import time

# Board Class
class Board():

    # Constructor
    def __init__(self):
        self.board = [i for i in range(1, 10)]

    def get_board(self):
        return self.board

    def show_board(self):
        print('_'*12)
        print('|', self.board[0], '|', self.board[1], '|', self.board[2])
        print('|', self.board[3], '|', self.board[4], '|', self.board[5])
        print('|', self.board[6], '|', self.board[7], '|', self.board[8])
        return ''

    # change the specified board postion
    # with the specified replacement
    def update_board(self, position, replacement):
        if type(position) != int:
            return 'Invalid input'

        else:
            self.board[position - 1] = replacement
            return self.board

    # store the diagonals of the board in a list
    # where the first element is a list of the diagonal running left to right
    # and the second element is a list of the diagonal running right to left
    def create_diagonals(self):

        first_diagonal = [self.board[0], self.board[4], self.board[8]]
        second_diagonal = [self.board[2], self.board[4], self.board[6]]
        diagonals = [first_diagonal, second_diagonal]

        return diagonals

    # store the columns of the board in a list
    # where each of the three elements is one of the columns
    # from left to right

    def create_cols(self):

        first_col = [self.board[0], self.board[3], self.board[6]]
        second_col = [self.board[1], self.board[4], self.board[7]]
        third_col = [self.board[2], self.board[5], self.board[8]]
        cols = [first_col, second_col, third_col]
        return cols

    def create_rows(self):
        first_row = self.board[0:3]
        second_row = self.board[3:6]
        third_row = self.board[6:]
        rows = [first_row, second_row, third_row]
        return rows

    # check if the board was solved
    def check_solved(self):
        cols = self.create_cols()
        rows = self.create_rows()
        diagonals = self.create_diagonals()

    # loop through each of the rows to see if any have
    # three consective 'X's or 'O's
        for row in rows:
            if row.count('X') == 3 or row.count('O') == 3:
                return True

    # loop through the columns just as we did for rows

        for column in cols:
            if column.count('X') == 3 or column.count('O') == 3:
                return True

        for diagonal in diagonals:
            if diagonal.count('X') == 3 or diagonal.count('O') == 3:
                return True

        return False

    # check to see whether their is a tie and neither player can win
    def check_tied(self):
        # check to see if both an X and O occur in each of the rows
        # if not, return False

        cols = self.create_cols()
        rows = self.create_rows()
        diagonals = self.create_diagonals()
        for row in rows:
            if 'X' not in row or 'O' not in row:
                return False

        # loop through the columns just as we did for the rows
        for column in cols:
            if 'X' not in column or 'O' not in column:
                return False

        for diagonal in diagonals:
            if 'X' not in diagonal or 'O' not in diagonal:
                return False

    # if we have passed all of the tests so far
    # it must still be possible to win
        return True

# Player Class


class Player():

    def __init__(self, player_symbol, opponent_symbol):
        self.player_symbol = player_symbol
        self.opponent_symbol = opponent_symbol

    # check if the player's opponent can win
    # with a single move
    def check_opponent_about_to_win(self, board_object):
        rows = board_object.create_rows()
        cols = board_object.create_cols()
        diagonals = board_object.create_diagonals()
        # check if there is a row such that the opponent has taken two spots
        # and the player has taken none
        for row in rows:
            if row.count(self.opponent_symbol) == 2 and row.count(self.player_symbol) == 0:
                for position in row:
                    if type(position) == int:
                        return position

        # do the same for each column
        for column in cols:
            if column.count(self.opponent_symbol) == 2 and column.count(self.player_symbol) == 0:
                for position in column:
                    if type(position) == int:
                        return position

        # do the same for each diagonal
        for diagonal in diagonals:
            if diagonal.count(self.opponent_symbol) == 2 and diagonal.count(self.player_symbol) == 0:
                for position in diagonal:
                    if type(position) == int:
                        return position

        # the opponent can not win
        return False

    def count_ways_to_win(self, position, board_object):

        # create a variable ways_to_win that stores the number of
        # possible rows of three from a position
        ways_to_win = 0

        rows = board_object.create_rows()
        cols = board_object.create_cols()
        diagonals = board_object.create_diagonals()

        for row in rows:
            if position in row:
                if self.opponent_symbol not in row:
                    ways_to_win += 1

        for column in cols:
            if position in column:
                if self.opponent_symbol not in column:
                    ways_to_win += 1

        for diagonal in diagonals:
            if position in diagonal:
                if self.opponent_symbol not in diagonal:
                    ways_to_win += 1

        return ways_to_win

    # find the position with the most possible ways to win
    # for a given player
    def find_best_spot(self, board_object):

        best_spot = None
        most_ways_to_win = 0

        # make sure to only loop through positions that are still available
        # that is, only positions that are still labeled with an integer
        spots_left = [i for i in board_object.get_board() if type(i) == int]

        for position in spots_left:
            ways_to_win = self.count_ways_to_win(position, board_object)
            if ways_to_win > most_ways_to_win:
                most_ways_to_win = ways_to_win
                best_spot = position

        return best_spot


# User Class inherited from Player
class User(Player):

    def __init__(self, user_symbol, computer_symbol):
        Player.__init__(self, user_symbol, computer_symbol)

    def move(self, board):
        # store the position chosen by the user
        user_input = input('Pick a space: ')

        try:
            position = int(user_input)

        except:
            return None

        # check to see whether the specified position actually lies on the board
        if not position in board.get_board():
            return None

        return position

# Computer Class (AI player) inherited from Player


class Computer(Player):

    def __init__(self, computer_symbol, user_symbol):
        Player.__init__(self, computer_symbol, user_symbol)

    def move(self, opponent, board):

        # check if there is a position open that will allow the computer to win

        if opponent.check_opponent_about_to_win(board):
            best_spot = opponent.check_opponent_about_to_win(board)
            board.update_board(best_spot, self.player_symbol)
            return board.show_board()

        if self.check_opponent_about_to_win(board):
            best_spot = self.check_opponent_about_to_win(board)
            board.update_board(best_spot, self.player_symbol)
            return board.show_board()

        if self.find_best_spot(board):
            best_spot = self.find_best_spot(board)
            board.update_board(best_spot, self.player_symbol)
            return board.show_board()

        # if we have not reached a return statement yet, then the computer can no longer win
        # even though the game is still not over.
        # In this case, we want to pretend we are the user and take their best spot

        best_spot = opponent.find_best_spot(board)
        board.update_board(best_spot, self.player_symbol)
        return board.show_board()


def test2():
    user = User('X', 'O')
    computer = Computer('O', 'X')
    board = Board()
    print(board.show_board())
    for i in range(5):
        print(user.move(board))
        print(computer.move(user, board))

# Game Class


class Game():

    def __init__(self):
        symbols = ['X', 'O']
        self.user_symbol = random.choice(symbols)
        self.computer_symbol = [i for i in symbols if i != self.user_symbol][0]

    def check_game_over(self, board):
        if board.check_solved():
            return True

        if board.check_tied():
            return True

        return False

    def main(self):
        # Create the game objects
        board = Board()
        user = User(self.user_symbol, self.computer_symbol)
        computer = Computer(self.computer_symbol, self.user_symbol)
        players = [user, computer]
        # randomly assign game symbols ('X' and 'O')
        first_player = random.choice(players)
        second_player = [i for i in players if i != first_player]

        print("Welcome to the world's best game of tic tac toe. Your symbol is " + self.user_symbol)
        print(board.show_board())

        if first_player == user:
            print('You start!')

        else:
            print('You go second!')

        next_move = True
        last_move = True
        # keep playing until the game is over
        while not self.check_game_over(board):
            if first_player == user:
                next_move = user.move(board)
                if next_move:
                    board.update_board(next_move, self.user_symbol)

                if self.check_game_over(board):
                    break

                # make sure the computer only takes a move
                # if the player made a valid mov
                if next_move:
                    computer.move(user, board)

            else:
                if last_move:
                    computer.move(user, board)

                if self.check_game_over(board):
                    break

                last_move = user.move(board)
                if last_move:
                    board.update_board(last_move, self.user_symbol)

        print("Game over")
        # Don't crash immediately
        time.sleep(5)


# play the game
if __name__ == '__main__':
    game = Game()
    game.main()
