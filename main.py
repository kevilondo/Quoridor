from board import Board
from game import Game

if __name__ == '__main__':
    game = Game()
    board = Board(game)
    board.draw_board()
    