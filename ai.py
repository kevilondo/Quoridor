from typing import TYPE_CHECKING
import random
import constants

if TYPE_CHECKING:
    from board import Board
    from player import Player

class AI:
    def __init__(self, board: "Board", player: "Player"):
        self.board = board
        self.player = player

    def make_move(self):
        self.board.move_pawn(self.player.pos[0], self.player.pos[1])
        possible_moves = self.board.game.possible_moves_for_turn
        move_to_play = possible_moves[random.randint(0, possible_moves.__len__() - 1)]
        self.board.move_pawn(move_to_play[0], move_to_play[1])