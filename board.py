import tkinter as tk
from typing import TYPE_CHECKING
from constants import MARGIN, CELL_SIZE, BOARD_SIZE
from pathfinding import PathFinding

if TYPE_CHECKING:
    from game import Game

class Board:
    def __init__(self, game: "Game"):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Quoridor")
        self.canvas_size = MARGIN * 2 + CELL_SIZE * BOARD_SIZE
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg='white')

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Control-Button-1>", self.on_right_click)

    def draw_board(self):
        self.canvas.pack()

        for idx, row in enumerate(range(BOARD_SIZE)):
            if idx == 0 or idx == BOARD_SIZE - 1:
                fill_color = "#bfbaba"
            else:
                fill_color = "#f0d9b5"
            for col in range(BOARD_SIZE):
                x0 = MARGIN + col * CELL_SIZE
                y0 = MARGIN + row * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, outline='gray', fill=fill_color)

        for player in [self.game.player1, self.game.player2]:
            self.draw_pawn(player.pos[0], player.pos[1], player.color)

        self.root.mainloop()

    def draw_pawn(self, row = None, col = None, color = "blue"):
        if col is None or row is None:
            return
        
        x0 = MARGIN + col * CELL_SIZE + CELL_SIZE // 4
        y0 = MARGIN + row * CELL_SIZE + CELL_SIZE // 4
        x1 = x0 + CELL_SIZE // 2
        y1 = y0 + CELL_SIZE // 2
    
        self.canvas.create_oval(x0, y0, x1, y1, fill=color, tags="pawn-"+color)

    def move_pawn(self, row, col):

        if self.game.possible_wall_placement_highlighted:
            return

        player = self.game.get_player_by_turn()

        if ((row, col) == player.pos):
        
            if self.game.possible_moves_highlighted == True:
                self.canvas.delete("possible_moves")
                self.game.possible_moves_highlighted = False
                self.game.possible_moves_for_turn = []

                return
            
            self.game.possible_moves_for_turn = self.game.determine_next_possible_moves(self, row, col)
            self.draw_possible_grids(self.game.possible_moves_for_turn)
            self.game.possible_moves_highlighted = True
            self.game.possible_wall_placement_highlighted = False
            self.game.possible_wall_placements = []
            self.canvas.delete("possible_wall_placement")

    
        if self.game.possible_moves_highlighted == True and (row, col) in self.game.possible_moves_for_turn:
            self.canvas.delete("pawn-"+player.color)
            self.draw_pawn(row, col, player.color)
            player.pos = (row, col)
            self.canvas.delete("possible_moves")
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

    def is_winning_row(self, player, position=None):
        position = position if position is not None else player.pos
        
        if (player == self.game.player1 and position[0] == 0) or (player == self.game.player2 and position[0] == BOARD_SIZE - 1):
            return True
        
        return False

    def draw_possible_grids(self, possible_moves, tags="possible_moves"):
        for move in possible_moves:
            row, col = move[0], move[1]
            x0 = MARGIN + col * CELL_SIZE
            y0 = MARGIN + row * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE

            self.canvas.create_rectangle(x0, y0, x1, y1, outline='green', width=3, tags=tags)

    def draw_wall(self, walls_built):
    # if row is the same, then it thickens the top border of both cells,
    # if col is the same, then it thickens the right border of both cells
        for wall in walls_built:
            if wall[0][1] == wall[1][1]:
                for cell in wall:
                    row, col = cell[0], cell[1]
                    # #if we are not at the end of the board (the. last column on the right), draw the wall on the right side, else draw it on the left

                    x0 = (MARGIN * 2 + 15) + col * CELL_SIZE
                    y0 = MARGIN + row * CELL_SIZE
                    x1 = x0 + CELL_SIZE / 5
                    y1 = y0 + CELL_SIZE

                    self.canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill='brown', tags="wall")
            else:
                for cell in wall:
                    row, col = cell[0], cell[1]
                    if row == 0:
                        row = 1

                    x0 = MARGIN + col * CELL_SIZE
                    y0 = MARGIN + row * CELL_SIZE
                    x1 = x0 + CELL_SIZE
                    y1 = y0 + CELL_SIZE / 5

                    self.canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill='brown', tags="wall")

    def on_click(self, event):
        col = (event.x - MARGIN) // CELL_SIZE
        row = (event.y - MARGIN) // CELL_SIZE

        self.move_pawn(row, col)

    def on_right_click(self, event):
        col = (event.x - MARGIN) // CELL_SIZE
        row = (event.y - MARGIN) // CELL_SIZE

        self.set_wall((row, col))

    def set_wall(self, clicked_cell_position):

        if not self.game.can_build_wall():
            print("YOU'RE OUT OF WALLS!")
            return

        #clicked_cell_position != player_1.pos and clicked_cell_position != player_2.pos
        if self.is_within_bounds(clicked_cell_position):

            if self.game.possible_wall_placement_highlighted == True:
                if clicked_cell_position not in self.game.possible_wall_placements:
                    self.canvas.delete("possible_wall_placement")
                    self.game.possible_wall_placement_highlighted = False
                    self.game.cells_to_block = []

                    return
                else:
                    self.game.cells_to_block.append(clicked_cell_position)
                    self.game.cells_to_block = self.game.sanitize_cells_to_block()

                    if self.is_wall_already_built(self.game.cells_to_block):
                        print("Wall already built here")

                        return
                    
                    self.canvas.delete("possible_wall_placement")
                    self.game.possible_wall_placement_highlighted = False
                    self.game.possible_wall_placements = []

                    self.game.walls_built.append(self.game.cells_to_block)
                    #illegal wall check
                    pf = PathFinding()
                    if not pf.is_exit_possible_for_player_1(self) or not pf.is_exit_possible_for_player_2(self):
                        self.game.walls_built.pop()
                        self.game.cells_to_block = []
                        print("ILLEGAL WALL!!!!!")
                        return

                    self.draw_wall([self.game.cells_to_block])
                    self.game.reduce_walls()
                    self.game.cells_to_block = []
                    self.game.switch_turn()
                    self.game.trigger_ai(self)

                    return

            self.game.possible_wall_placements = self.game.determine_next_possible_wall_placement(self, clicked_cell_position)
            self.game.cells_to_block.append(clicked_cell_position)
            self.draw_possible_grids(self.game.possible_wall_placements, tags="possible_wall_placement")
            self.game.possible_wall_placement_highlighted = True

    def is_position_vertical(self, cells):
        return cells[0][1] == cells[1][1]

    def is_position_horizontal(self, cells):
        return cells[0][0] == cells[1][0]

    def is_wall_already_built(self, cells_to_block):
        result = False

        for wall in self.game.walls_built:
            wall_point_a, wall_point_b = wall[0], wall[1]

            #this simply means that you can't have one wall cutting through another. like a + shaped block. but you can do a T shaped
            #doesn't matter which wall was created first, horizontal or vertical, we just don't want this shape "+" and wall that extends an existing one like this ---

            is_wall_extending_downward = max(cells_to_block[0][0], cells_to_block[1][0]) > max(wall_point_a[0], wall_point_b[0])

            is_wall_extending_or_cutting = (max(wall_point_a, wall_point_b) == min(cells_to_block[0], cells_to_block[1])) or (min(wall_point_a, wall_point_b) == max(cells_to_block[0], cells_to_block[1]))
            if is_wall_extending_or_cutting and not is_wall_extending_downward:
                result = True

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
    