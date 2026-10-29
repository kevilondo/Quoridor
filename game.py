from constants import MAX_WALLS, PLAYER_1, PLAYER_2, BOARD_SIZE, BLUE, RED
from player import Player
from typing import TYPE_CHECKING
from ai import AI

if TYPE_CHECKING:
    from board import Board

class Game:
    def __init__(self):
        self.possible_moves_highlighted = False
    
        self.player1 = Player((8, 4), BLUE, True)
        self.player2 = Player((0, 4), RED)
    
        self.turn = PLAYER_1
    
        self.cells_to_block = []
        self.possible_wall_placement_highlighted = False
        self.possible_wall_placements = []
        self.walls_built = []
    
        self.possible_moves_for_turn = []
        self.ai_player = PLAYER_1 if self.player1.ai_controlled else PLAYER_2

#Since we cannot draw a wall on the edge of the board, we need to sanitize the cells to block if they are on the edge of the board and block the next cell inwards instead
    def sanitize_cells_to_block(self):
        cells = []

        first_cell = self.cells_to_block[0]
        next_cell = self.cells_to_block[1]

        if first_cell[0] == 0 and next_cell[0] == 0:
            first_cell = (first_cell[0] + 1, first_cell[1])
            next_cell = (next_cell[0] + 1, next_cell[1])

        if first_cell[1] == BOARD_SIZE - 1 and next_cell[1] == BOARD_SIZE - 1:
            first_cell = (first_cell[0], first_cell[1] - 1)
            next_cell = (next_cell[0], next_cell[1] - 1)

        cells.append(first_cell)
        cells.append(next_cell)

        return cells

    def reduce_walls(self):
        if self.turn == PLAYER_1:
            self.player1.walls -= 1
        else:
            self.player2.walls -= 1

    def can_build_wall(self):
        player = self.player1

        if self.turn == PLAYER_2:
            player = self.player2

        return player.walls > 0

    def switch_turn(self):
        if self.turn == PLAYER_1:
            self.turn = PLAYER_2
        else:
            self.turn = PLAYER_1

    def get_player_by_turn(self):
        if self.turn == PLAYER_1:
            return self.player1
        else:
            return self.player2

    def get_opponent_on_this_turn(self):
        if self.turn == PLAYER_1:
            return self.player2
        else:
            return self.player1

    def trigger_ai(self, board: "Board"):
        player = self.get_player_by_turn()
        if player.ai_controlled:
            ai = AI(board, player)
            ai.make_move()

    def get_opposing_player(self, player):
        if player.color == self.player1.color:
            return self.player2
        else:
            return self.player1

    def get_player_by_color(self, color):
        if self.player1.color == color:
            return self.player1
        else:
            return self.player2
    
    def clone(self):
        new_game = Game()
        new_game.player1 = self.player1
        new_game.player2 = self.player2
        new_game.turn = self.turn
        new_game.cells_to_block = self.cells_to_block.copy()
        new_game.possible_wall_placement_highlighted = self.possible_wall_placement_highlighted
        new_game.possible_wall_placements = self.possible_wall_placements.copy()
        new_game.walls_built = self.walls_built.copy()
        new_game.possible_moves_for_turn = self.possible_moves_for_turn.copy()
        return new_game
