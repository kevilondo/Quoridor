from board import Board
from game import Game
from ui import UI

if __name__ == '__main__':
    game = Game()
    board = Board(game)
    print(game.turn, game.ai_player)
    if game.ai_player == game.turn:
        game.trigger_ai(board)
    ui = UI(board)
    ui.draw_board()
    