from board import Board
from game import Game
from ui import UI

if __name__ == '__main__':
    game = Game()
    board = Board(game)
    ui = UI(board)
    ui.draw_board()
    