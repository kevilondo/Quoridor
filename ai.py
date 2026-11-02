from typing import TYPE_CHECKING
from pathfinding import PathFinding
from constants import AI_DEPTH, BEST_SCORE_FOR_AI, BOARD_SIZE
from board import Board
from player import Player
from copy import deepcopy

if TYPE_CHECKING:
    from player import Player

class AI:
    def __init__(self, board: "Board", player: "Player"):
        self.board = board
        self.player = player

    def set_wall(self, position):
        self.board.set_wall(position[0])
        self.board.set_wall(position[1])

    def make_move(self):
        opponent = self.board.game.get_opposing_player(self.player)

        move_to_play = self.minimax(self.player.pos, opponent.pos, AI_DEPTH, True)
        move_score = move_to_play[0]
        wall_to_place_and_score = self.wall_placement_decision()
        wall_score = wall_to_place_and_score[0]
        wall_to_place = wall_to_place_and_score[1]

        if wall_score > move_score:
            self.set_wall(wall_to_place)

            return

        position = move_to_play[1]
        self.board.move_pawn(self.player.pos[0], self.player.pos[1])
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

    def wall_placement_decision(self):
        opponent = self.board.game.get_opposing_player(self.player)
        opponent_distance_to_goal_and_path = PathFinding().path_and_distance_from_goal(self.board, opponent.pos, opponent)
        opponent_path = opponent_distance_to_goal_and_path[1]

        best_wall_placement = None
        best_score = float('-inf')

        for cell in opponent_path:
            possible_walls = self.board.determine_next_possible_wall_placement(cell)

            for wall_position in possible_walls:
                temp_game = self.board.game.clone()
                temp_game.player1 = Player(self.board.game.player1.pos, self.board.game.player1.color, self.board.game.player1.ai_controlled)
                temp_game.player2 = Player(self.board.game.player2.pos, self.board.game.player2.color, self.board.game.player2.ai_controlled)
                temp_game.player1.walls = self.board.game.player1.walls
                temp_game.player2.walls = self.board.game.player2.walls
                temp_board = Board(temp_game)
                temp_board.set_wall(cell)
                cells_to_block = temp_board.set_wall(wall_position)

                if cells_to_block.__len__() == 0:
                    continue

                score = self.evaluate_wall(temp_board)

                if score > best_score:
                    best_score = score
                    best_wall_placement = cells_to_block

        return best_score, best_wall_placement

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

    def evaluate_wall(self, board):
        opponent = board.game.get_opposing_player(self.player)
        ai_player = board.game.player1 if board.game.player1.ai_controlled == True else board.game.player2

        path = PathFinding()

        distance_to_goal = path.distance_from_position_to_goal(board, ai_player.pos, ai_player)
        distance_opponent_to_goal = path.distance_from_position_to_goal(board, opponent.pos, opponent)

        return (distance_opponent_to_goal - distance_to_goal) + ((opponent.walls - ai_player.walls) // 2)
