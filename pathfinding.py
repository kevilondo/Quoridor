from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board

class PathFinding:
    def is_exit_possible(self, board: "Board", player):
        game = board.game
        visited = []
        cells_to_visit = []

        cells_to_visit = game.determine_next_possible_move(board, player["pos"][0], player["pos"][1])
        visited.append(player["pos"])

        while cells_to_visit.__len__() > 0:
            cell = cells_to_visit[0]

            if (cell[0] == 0 and player == game.player1) or (cell[0] == 8 and player == game.player2): #if we reach the destination, then an exit is indeed possible
                return True
            
            if cell in visited:
                cells_to_visit.remove(cell)
                continue

            next_possible_cells = game.determine_next_possible_move(board, cell[0], cell[1])

            if next_possible_cells.__len__() > 0:

                for cell_to_insert in next_possible_cells:
                    cells_to_visit.insert(cells_to_visit.index(cell), cell_to_insert)

                visited.append(cell)
                cells_to_visit.remove(cell)

        return False

    def is_exit_possible_for_player_1(self, board: "Board"):
        return self.is_exit_possible(board, board.game.player1)

    def is_exit_possible_for_player_2(self, board: "Board"):
            return self.is_exit_possible(board, board.game.player2)
        