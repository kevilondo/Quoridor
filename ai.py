from typing import TYPE_CHECKING
from pathfinding import PathFinding
from constants import AI_DEPTH, BEST_SCORE_FOR_AI
import copy

if TYPE_CHECKING:
    from board import Board
    from player import Player

class AI:
    def __init__(self, board: "Board", player: "Player"):
        self.board = board
        self.player = player

    def set_wall(self, position):
        self.board.set_wall(position[0])
        self.board.set_wall(position[1])

    def make_move(self):
        self.board.move_pawn(self.player.pos[0], self.player.pos[1])
        opponent = self.board.game.get_opposing_player(self.player)
        move_to_play = self.minimax(self.player.pos, opponent.pos, AI_DEPTH, True)

        position = move_to_play[1]
        self.board.move_pawn(position[0], position[1])

    def minimax(self, position, opponent_position, depth, is_maximizing_player):
        if self.board.is_winning_row(self.player, position):
            return BEST_SCORE_FOR_AI, position

        opponent = self.board.game.get_opposing_player(self.player)

        if self.board.is_winning_row(opponent, opponent_position):
            return -BEST_SCORE_FOR_AI, opponent_position
        
        if depth == 0:
            return self.evaluate_position(position, opponent_position), None

        if is_maximizing_player:
            max_eval = float('-inf')
            best_move = None

            for move in self.board.determine_next_possible_moves(position[0], position[1]):
                evaluation = self.minimax(move, opponent_position, depth - 1, False)[0]
                
                if max_eval < evaluation or self.board.is_winning_row(self.player, move):
                    max_eval = evaluation
                    best_move = move

            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None

            for move in self.board.determine_next_possible_moves(opponent_position[0], opponent_position[1]):
                evaluation = self.minimax(position, move, depth - 1, True)[0]
                
                if min_eval > evaluation or self.board.is_winning_row(opponent, move):
                    min_eval = evaluation
                    best_move = move

            return min_eval, best_move

    def evaluate_position(self, position, opponent_position):

        opponent = self.board.game.get_opposing_player(self.player)

        if self.board.is_winning_row(self.player, position):
            return BEST_SCORE_FOR_AI

        if self.board.is_winning_row(opponent, opponent_position):
            return -BEST_SCORE_FOR_AI

        path = PathFinding()

        distance_to_goal = path.distance_from_position_to_goal(self.board, position, self.player)
        distance_opponent_to_goal = path.distance_from_position_to_goal(self.board, opponent_position, opponent)

        return (distance_opponent_to_goal - distance_to_goal)
        