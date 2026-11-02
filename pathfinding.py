from typing import TYPE_CHECKING
from collections import deque

if TYPE_CHECKING:
    from board import Board

class PathFinding:
    def is_exit_possible(self, board: "Board", player):
        game = board.game
        visited = {player.pos}
        cells_to_visit = deque([player.pos])

        while cells_to_visit:
            cell = cells_to_visit.popleft()

            if (cell[0] == 0 and player == game.player1) or (cell[0] == 8 and player == game.player2): #if we reach the destination, then an exit is indeed possible
                return True

            for neighbor in board.determine_next_possible_moves(cell[0], cell[1]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    cells_to_visit.append(neighbor)

        return False

    def is_exit_possible_for_player_1(self, board: "Board"):
        return self.is_exit_possible(board, board.game.player1)

    def is_exit_possible_for_player_2(self, board: "Board"):
            return self.is_exit_possible(board, board.game.player2)

    def distance_from_position_to_goal(self, board: "Board", position, player):
        distance, _ = self.path_and_distance_from_goal(board, position, player)
        return distance

    def path_and_distance_from_goal(self, board: "Board", position, player):
        visited = [position]
        cells_to_visit = [(position, 0)]
        parent = {position: None}

        while cells_to_visit.__len__() > 0:
            cell, distance = cells_to_visit.pop(0)
            if board.is_winning_row(player, cell):
                path = []
                while cell is not None:
                    path.append(cell)
                    cell = parent[cell]
                path.reverse()

                return distance, path

            neighbors = board.determine_next_possible_moves(cell[0], cell[1])
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.append(neighbor)
                    parent[neighbor] = cell
                    cells_to_visit.append((neighbor, distance + 1))
        return -1, []