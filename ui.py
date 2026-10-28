from constants import BOARD_SIZE, MARGIN, CELL_SIZE
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board

class UI:
    def __init__(self, board: "Board"):
        self.root = tk.Tk()
        self.board = board
        self.game = board.game
        self.root.title("Quoridor")
        self.canvas_size = MARGIN * 2 + CELL_SIZE * BOARD_SIZE
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg='white')

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Control-Button-1>", self.on_right_click)

        for pawn in [self.game.player1, self.game.player2]:
            pawn.subscribe("pos", self.on_pawn_moved)
            pawn.subscribe("walls", self.on_wall_set)

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

    def draw_possible_grids(self, possible_moves, tags="possible_moves"):
        for move in possible_moves:
            row, col = move[0], move[1]
            x0 = MARGIN + col * CELL_SIZE
            y0 = MARGIN + row * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE

            self.canvas.create_rectangle(x0, y0, x1, y1, outline='green', width=3, tags=tags)

    def draw_wall(self, wall):
        # if row is the same, then it thickens the top border of both cells,
        # if col is the same, then it thickens the right border of both cells
        
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
            self.game.possible_wall_placement_highlighted = False
            self.canvas.delete("possible_wall_placement")

            col = (event.x - MARGIN) // CELL_SIZE
            row = (event.y - MARGIN) // CELL_SIZE

            can_move_pawn = self.board.move_pawn(row, col)

            if self.game.possible_moves_for_turn.__len__() > 0:
                self.draw_possible_grids(self.game.possible_moves_for_turn)
                self.canvas.delete("possible_wall_placement")
            elif self.game.possible_moves_highlighted == False and can_move_pawn == True:
                self.canvas.delete("possible_moves")
                player = self.game.get_player_by_turn()
                self.canvas.delete("pawn-"+player.color)
                self.draw_pawn(row, col, player.color)
            else:
                self.canvas.delete("possible_moves")
                self.canvas.delete("possible_wall_placement")
    
    def on_right_click(self, event):
        # print("Right click detected: " + str(self.game.possible_moves_highlighted))
        self.game.possible_moves_highlighted = False
        self.canvas.delete("possible_moves")

        col = (event.x - MARGIN) // CELL_SIZE
        row = (event.y - MARGIN) // CELL_SIZE

        wall = self.board.set_wall((row, col))

        if wall.__len__() > 0:
            self.draw_wall(wall)
            self.canvas.delete("possible_wall_placement")
        elif self.game.possible_wall_placement_highlighted == True:
            self.draw_possible_grids(self.game.possible_wall_placements, tags="possible_wall_placement")
        else:
            self.canvas.delete("possible_wall_placement")

    def on_pawn_moved(self, player):
        self.canvas.delete("pawn-"+player.color)
        self.draw_pawn(player.pos[0], player.pos[1], player.color)

    def on_wall_set(self):
        wall = self.board.game.walls_built[self.board.game.walls_built.__len__() - 1]
        self.draw_wall(wall)
        self.canvas.delete("possible_wall_placement")
        self.canvas.delete("possible_moves")

