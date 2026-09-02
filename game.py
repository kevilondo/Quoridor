from board import Board
from constants import MAX_WALLS, PLAYER_1, PLAYER_2, BOARD_SIZE

class Game:
    def __init__(self):
        self.possible_moves_highlighted = False
    
        self.player1 = {"pos": (8, 4), "color": "blue", "walls": MAX_WALLS}
        self.player2 = {"pos": (0, 4), "color": "red", "walls": MAX_WALLS}
    
        self.turn = PLAYER_1
    
        self.cells_to_block = []
        self.possible_wall_placement_highlighted = False
        self.possible_wall_placements = []
        self.walls_built = []
    
        self.possible_moves_for_turn = []

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
            self.player1["walls"] -= 1
        else:
            self.player2["walls"] -= 2

    def can_build_wall(self):
        player = self.player1

        if self.turn == PLAYER_2:
            player = self.player2

        return player["walls"] > 0

    def determine_next_possible_wall_placement(self, board, clicked_cell_position):
        possible_wall_placements = []
        row, col = clicked_cell_position
        up = (row - 1, col)
        down = (row + 1, col)
        left = (row, col - 1)
        right = (row, col + 1)

        if board.is_within_bounds(up):
            possible_wall_placements.append(up)
        if board.is_within_bounds(down):
            possible_wall_placements.append(down)
        if board.is_within_bounds(left):
            possible_wall_placements.append(left)
        if board.is_within_bounds(right):
            possible_wall_placements.append(right)

        return possible_wall_placements

    def determine_next_possible_move(self, board, row, col):
        possible_moves = []

        up = self.next_possible_cell_by_direction(board, row, col, "up")
        down = self.next_possible_cell_by_direction(board, row, col, "down")
        left = self.next_possible_cell_by_direction(board, row, col, "left")
        right = self.next_possible_cell_by_direction(board, row, col, "right")

        if up != None:
            possible_moves.append(up)

        if down != None:
            possible_moves.append(down)

        if left != None:
            possible_moves.append(left)

        if right != None:
            possible_moves.append(right)

        return possible_moves

    def next_possible_cell_by_direction(self, board, row, col, direction):
        target_direction = None
        better_cell = None

        if direction == "up":
            target_direction = (row - 1, col)
            better_cell = (row - 2, col)
        elif direction == "down":
            target_direction = (row + 1, col)
            better_cell = (row + 2, col)
        elif direction == "left":
            target_direction = (row, col - 1)
            better_cell = (row, col - 2)
        elif direction == "right":
            target_direction = (row, col + 1)
            better_cell = (row, col + 2)

        if self.player2["pos"] == target_direction:
            next_move = better_cell
            if board.is_within_bounds(next_move):
                return next_move
            else:
                return None
            
        if not board.is_within_bounds(target_direction) or board.is_blocked_by_wall((row, col), target_direction):
            return None

        return target_direction
    