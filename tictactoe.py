#--------------------------------------------------------------------
# Tic Tac Toe game
#
# Designed so that the computer always wins or ties
# Uses the minimax algorithm with alpha beta pruning to calculate the
#  next best move
#
# Written in Flask framework and AngularJS for the frontend
#--------------------------------------------------------------------
from flask import Flask, render_template, jsonify, request
from game import Game

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    post = request.get_json()

    game = Game()
    game.board = post.get('board')
    game.player = post.get('player')
    game.computer = post.get('computer')

    # Check if player won
    if game.has_won(game.player):
        return jsonify(tied = False, computer_wins = False, player_wins = True, board = game.board)
    elif game.is_board_full():
        return jsonify(tied = True, computer_wins = False, player_wins = False, board = game.board)

    # Calculate computer move
    computer_move = game.calculate_move()

    # Make the next move
    game.make_computer_move(computer_move['row'], computer_move['col'])

    # Check if computer won
    if game.has_won(game.computer):
        return jsonify(computer_row = computer_move['row'], computer_col = computer_move['col'],
                       computer_wins = True, player_wins = False, tied=False, board = game.board)
    # Check if game is over
    elif game.is_board_full():
        return jsonify(computer_row = computer_move['row'], computer_col = computer_move['col'],
                       computer_wins = False, player_wins = False, tied=True, board=game.board)

    # Game still going
    return jsonify(computer_row = computer_move['row'], computer_col = computer_move['col'],
                   computer_wins = False, player_wins = False, board = game.board)

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')