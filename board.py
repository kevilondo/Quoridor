from typing import TYPE_CHECKING
from constants import MARGIN, CELL_SIZE, BOARD_SIZE
from pathfinding import PathFinding

if TYPE_CHECKING:
    from game import Game

class Board:
    def __init__(self, game: "Game"):
        self.game = game

    def move_pawn(self, row, col):

        if self.game.possible_wall_placement_highlighted:
            return False

        player = self.game.get_player_by_turn()

        if ((row, col) == player.pos):
        
            if self.game.possible_moves_highlighted == True:
                self.game.possible_moves_highlighted = False
                self.game.possible_moves_for_turn = []
                self.game.cells_to_block = []

                return False
            
            self.game.possible_moves_for_turn = self.determine_next_possible_moves(row, col)

            self.game.possible_moves_highlighted = True
            self.game.possible_wall_placement_highlighted = False
            self.game.possible_wall_placements = []
            self.game.cells_to_block = []
    
        if self.game.possible_moves_highlighted == True and (row, col) in self.game.possible_moves_for_turn:

            player.pos = (row, col)

            self.game.possible_moves_for_turn = []
            self.game.possible_moves_highlighted = False

            if self.is_winning_row(self.game.player1):
                print("win!")
                exit()
            elif self.is_winning_row(self.game.player2):
                print("player 2 win!")
                exit()

            self.game.switch_turn()
            self.game.trigger_ai(self)

            return True

        return False

    def is_winning_row(self, player, position=None):
        position = position if position is not None else player.pos
        
        if (player == self.game.player1 and position[0] == 0) or (player == self.game.player2 and position[0] == BOARD_SIZE - 1):
            return True
        
        return False

    def set_wall(self, clicked_cell_position):

        if not self.game.can_build_wall():
            print("YOU'RE OUT OF WALLS!")
            return []

        if self.is_within_bounds(clicked_cell_position):

            if self.game.possible_wall_placement_highlighted == True:
                if clicked_cell_position not in self.game.possible_wall_placements:

                    self.game.possible_wall_placement_highlighted = False
                    self.game.cells_to_block = []

                    return []
                else:
                    self.game.cells_to_block.append(clicked_cell_position)
                    self.game.cells_to_block = self.game.sanitize_cells_to_block()

                    if self.is_wall_already_built(self.game.cells_to_block):
                        print("Wall already built here")

                        return []
                    
                    self.game.possible_wall_placement_highlighted = False
                    self.game.possible_wall_placements = []

                    self.game.walls_built.append(self.game.cells_to_block)
                    #illegal wall check
                    pf = PathFinding()
                    if not pf.is_exit_possible_for_player_1(self) or not pf.is_exit_possible_for_player_2(self):
                        self.game.walls_built.pop()
                        self.game.cells_to_block = []
                        print("ILLEGAL WALL!!!!!")
                        return []

                    cells_to_block = self.game.cells_to_block
                    self.game.reduce_walls()
                    self.game.cells_to_block = []
                    self.game.switch_turn()
                    self.game.trigger_ai(self)

                    return cells_to_block

            self.game.possible_wall_placements = self.determine_next_possible_wall_placement(clicked_cell_position)
            self.game.cells_to_block.append(clicked_cell_position)
            self.game.possible_wall_placement_highlighted = True

            return []

    def is_position_vertical(self, cells):
        return cells[0][1] == cells[1][1]

    def is_position_horizontal(self, cells):
        return cells[0][0] == cells[1][0]

    def is_wall_already_built(self, cells_to_block):
        result = False

        for wall in self.game.walls_built:
            wall_point_a, wall_point_b = wall[0], wall[1]

            sorted_wall = sorted([wall_point_a, wall_point_b])
            sorted_cells_to_block = sorted(cells_to_block)

            if (sorted_wall == sorted_cells_to_block):
                result = True
                break

            if (self.is_position_vertical(sorted_wall) and self.is_position_vertical(sorted_cells_to_block)) or (self.is_position_horizontal(sorted_wall) and self.is_position_horizontal(sorted_cells_to_block)):
                if max(sorted_cells_to_block) == min(sorted_wall) or min(sorted_cells_to_block) == max(sorted_wall):
                    result = True
                    break

            if self.is_position_horizontal(sorted_wall) and self.is_position_vertical(sorted_cells_to_block):
                if max(sorted_cells_to_block) == min(sorted_wall):
                    result = True
                    break

            if self.is_position_vertical(sorted_wall) and self.is_position_horizontal(sorted_cells_to_block):
                if min(sorted_cells_to_block) == max(sorted_wall):
                    result = True
                    break

        return result

    def is_within_bounds(self, cell):
        row, col = cell

        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def is_blocked_by_wall(self, current_cell, target_cell):
        vertical_movement = self.is_position_vertical([current_cell, target_cell])
        horizontal_movement = self.is_position_horizontal([current_cell, target_cell])

        target_cell_wall_vertical = self.get_wall_for_cell_by_direction(target_cell, "vertical")
        target_cell_wall_horizontal = self.get_wall_for_cell_by_direction(target_cell, "horizontal")
        
        current_cell_wall_vertical = self.get_wall_for_cell_by_direction(current_cell, "vertical")
        current_cell_wall_horizontal = self.get_wall_for_cell_by_direction(current_cell, "horizontal")

        going_up = current_cell[0] > target_cell[0]
        going_down = current_cell[0] < target_cell[0]
        going_right = current_cell[1] < target_cell[1]
        going_left = current_cell[1] > target_cell[1]

        if vertical_movement:
            if (going_up and current_cell_wall_horizontal) or (going_down and target_cell_wall_horizontal):
                return True
            
        if horizontal_movement:
            if (going_right and current_cell_wall_vertical) or (going_left and target_cell_wall_vertical):
                return True

        return False

    def get_wall_for_cell_by_direction(self, cell, direction="horizontal"):
        index = None

        if direction == "horizontal":
            index = next(
                (i for i, wall in enumerate(self.game.walls_built) if cell in wall and self.is_position_horizontal(wall)), 
                None
            )
        elif direction == "vertical":
            index = next(
                (i for i, wall in enumerate(self.game.walls_built) if cell in wall and self.is_position_vertical(wall)), 
                None
            )
        else:
            return None
        
        if index == None:
            return None

        return self.game.walls_built[index]

    def get_all_grids(self):
        grids = []

        for i in range(0, BOARD_SIZE - 1):
            for j in range (0, BOARD_SIZE - 1):
                grids.append((i, j))

        return grids

    def determine_next_possible_wall_placement(self, clicked_cell_position):
        possible_wall_placements = []
        row, col = clicked_cell_position
        up = (row - 1, col)
        down = (row + 1, col)
        left = (row, col - 1)
        right = (row, col + 1)

        if self.is_within_bounds(up):
            possible_wall_placements.append(up)
        if self.is_within_bounds(down):
            possible_wall_placements.append(down)
        if self.is_within_bounds(left):
            possible_wall_placements.append(left)
        if self.is_within_bounds(right):
            possible_wall_placements.append(right)

        return possible_wall_placements

    def determine_next_possible_moves(self, row, col):
        target_positions = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]

        possible_moves = []

        for position in target_positions:
            if not self.is_within_bounds(position):
                continue

            if self.is_blocked_by_wall((row, col), position):
                continue

            if self.game.get_opponent_on_this_turn().pos != position:
                possible_moves.append(position)
            else:
                is_up = position[0] < row
                is_down = position[0] > row
                is_left = position[1] < col
                is_right = position[1] > col
                alternative_positions = []
                
                if is_up:
                    pos = (row - 2, col)
                    if self.is_within_bounds(pos) and not self.is_blocked_by_wall(position, pos):
                        possible_moves.append(pos)
                        continue
                    else:
                        alternative_positions = [(row - 1, col - 1), (row - 1, col + 1)]
                elif is_down:
                    pos = (row + 2, col)
                    if self.is_within_bounds(pos) and not self.is_blocked_by_wall(position, pos):
                        possible_moves.append(pos)
                        continue
                    else:
                        alternative_positions = [(row + 1, col - 1), (row + 1, col + 1)]
                elif is_left:
                    pos = (row, col - 2)
                    if self.is_within_bounds(pos) and not self.is_blocked_by_wall(position, pos):
                        possible_moves.append(pos)
                        continue
                    else:
                        alternative_positions = [(row - 1, col - 1), (row + 1, col - 1)]
                elif is_right:
                    pos = (row, col + 2)
                    if self.is_within_bounds(pos) and not self.is_blocked_by_wall(position, pos):
                        possible_moves.append(pos)
                        continue
                    else:
                        alternative_positions = [(row - 1, col + 1), (row + 1, col + 1)]

                for alternative_position in alternative_positions:
                    if self.is_within_bounds(alternative_position) and not self.is_blocked_by_wall(position, alternative_position):
                        possible_moves.append(alternative_position)

        return possible_moves
    