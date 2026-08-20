import tkinter as tk

BOARD_SIZE = 9
CELL_SIZE = 60
MARGIN = 40
MAX_WALLS = 10
PLAYER_1 = "player 1"
PLAYER_2 = "player 2"

root = tk.Tk()
root.title("Quoridor")
canvas_size = MARGIN * 2 + CELL_SIZE * BOARD_SIZE
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg='white')
possible_moves_highlighted = False

player_1 = {"pos": (8, 4), "color": "blue", "walls": MAX_WALLS}
player_2 = {"pos": (0, 4), "color": "red", "walls": MAX_WALLS}

turn = PLAYER_1

cells_to_block = []
possible_wall_placement_highlighted = False
possible_wall_placements = []
walls_built = []

possible_moves_for_turn = []

def draw_board():
    canvas.pack()

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
            canvas.create_rectangle(x0, y0, x1, y1, outline='gray', fill=fill_color)

    for player in [player_1, player_2]:
        draw_pawn(player["pos"][0], player["pos"][1], player["color"])

    root.mainloop()

def draw_pawn(row = None, col = None, color = "blue"):
    if col is None or row is None:
        return

    x0 = MARGIN + col * CELL_SIZE + CELL_SIZE // 4
    y0 = MARGIN + row * CELL_SIZE + CELL_SIZE // 4
    x1 = x0 + CELL_SIZE // 2
    y1 = y0 + CELL_SIZE // 2

    canvas.create_oval(x0, y0, x1, y1, fill=color, tags="pawn-"+color)

def on_click(event):
    col = (event.x - MARGIN) // CELL_SIZE
    row = (event.y - MARGIN) // CELL_SIZE

    move_pawn(row, col)

def on_right_click(event):
    col = (event.x - MARGIN) // CELL_SIZE
    row = (event.y - MARGIN) // CELL_SIZE

    set_wall((row, col))

def can_build_wall():
    player = player_1

    if turn == PLAYER_2:
        player = player_2

    return player["walls"] > 0

def set_wall(clicked_cell_position):
    global possible_wall_placement_highlighted
    global possible_wall_placements
    global cells_to_block
    global walls_built

    if not can_build_wall():
        print("YOU'RE OUT OF WALLS!")
        return

#clicked_cell_position != player_1["pos"] and clicked_cell_position != player_2["pos"]
    if is_within_bounds(clicked_cell_position):

        if possible_wall_placement_highlighted == True:
            if clicked_cell_position not in possible_wall_placements:
                canvas.delete("possible_wall_placement")
                possible_wall_placement_highlighted = False
                cells_to_block = []

                return
            else:
                cells_to_block.append(clicked_cell_position)
                cells_to_block = sanitize_cells_to_block(cells_to_block)

                if is_wall_already_built(cells_to_block):
                    print("Wall already built here")

                    return
                
                canvas.delete("possible_wall_placement")
                possible_wall_placement_highlighted = False
                possible_wall_placements = []

                walls_built.append(cells_to_block)
                draw_wall([cells_to_block])
                reduce_walls()
                cells_to_block = []

                return

        possible_wall_placements = determine_next_possible_wall_placement(clicked_cell_position)
        cells_to_block.append(clicked_cell_position)
        draw_possible_grids(possible_wall_placements, tags="possible_wall_placement")
        possible_wall_placement_highlighted = True

def sanitize_cells_to_block(cells_to_block):
    cells = []

    first_cell = cells_to_block[0]
    next_cell = cells_to_block[1]

    if first_cell[0] == 0 and next_cell[0] == 0:
        first_cell = (first_cell[0] + 1, first_cell[1])
        next_cell = (next_cell[0] + 1, next_cell[1])

    if first_cell[1] == BOARD_SIZE - 1 and next_cell[1] == BOARD_SIZE - 1:
        first_cell = (first_cell[0], first_cell[1] - 1)
        next_cell = (next_cell[0], next_cell[1] - 1)

    cells.append(first_cell)
    cells.append(next_cell)

    return cells

def reduce_walls():
    global player_1
    global player_2

    if turn == PLAYER_1:
        player_1["walls"] -= 1
    else:
        player_2["walls"] -= 2

def is_position_vertical(cells):
    return cells[0][1] == cells[1][1]

def is_position_horizontal(cells):
    return cells[0][0] == cells[1][0]

def is_wall_already_built(cells_to_block):
    global walls_built
    result = False

    for wall in walls_built:
        wall_point_a, wall_point_b = wall[0], wall[1]
        wall_row_sum = wall_point_a[0] + wall_point_b[0]
        ctb_row_sum = cells_to_block[0][0] + cells_to_block[1][0]
        wall_col_sum = wall_point_a[1] + wall_point_b[1]
        ctb_col_sum = cells_to_block[0][1] + cells_to_block[1][1]
        #this simply means that you can't have one wall cutting through another. like a + shaped block. but you can do a T shaped

        is_wall_vertical = is_position_vertical(wall)
        is_wall_horizontal = is_position_horizontal(wall)

        is_position_incorrect = (is_wall_vertical and ctb_row_sum > wall_row_sum) or (is_wall_horizontal and ctb_col_sum <= wall_col_sum)

        #check if new wall is extending the old one then reject it
        is_ctb_vertical = cells_to_block[0][1] == cells_to_block[1][1]
        is_ctb_horizontal = cells_to_block[0][0] == cells_to_block[1][0]
        have_same_column = cells_to_block[0][1] == cells_to_block[1][1] == wall_point_a[1] == wall_point_b[1]
        have_same_row = cells_to_block[0][0] == cells_to_block[1][0] == wall_point_a[0] == wall_point_b[0]
        is_new_wall_extending = (is_ctb_vertical and have_same_column) or (is_ctb_horizontal and have_same_row)


        if ((wall_point_a in cells_to_block or wall_point_b in cells_to_block) and (is_position_incorrect or is_new_wall_extending)):
            result = True

    return result

def determine_next_possible_wall_placement(clicked_cell_position):
    possible_wall_placements = []
    row, col = clicked_cell_position
    up = (row - 1, col)
    down = (row + 1, col)
    left = (row, col - 1)
    right = (row, col + 1)

    if is_within_bounds(up):
        possible_wall_placements.append(up)
    if is_within_bounds(down):
        possible_wall_placements.append(down)
    if is_within_bounds(left):
        possible_wall_placements.append(left)
    if is_within_bounds(right):
        possible_wall_placements.append(right)

    return possible_wall_placements

def draw_wall(walls_built):
    # if row is the same, then it thickens the top border of both cells,
    # if row is the same, then it thickens the right border of both cells
    for wall in walls_built:

        if wall[0][1] == wall[1][1]:
            for cell in wall:
                row, col = cell[0], cell[1]
                # #if we are not at the end of the board (the. last column on the right), draw the wall on the right side, else draw it on the left

                x0 = (MARGIN * 2 + 15) + col * CELL_SIZE
                y0 = MARGIN + row * CELL_SIZE
                x1 = x0 + CELL_SIZE / 5
                y1 = y0 + CELL_SIZE

                canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill='brown', tags="wall")
        else:
            for cell in wall:
                row, col = cell[0], cell[1]
                if row == 0:
                    row = 1

                x0 = MARGIN + col * CELL_SIZE
                y0 = MARGIN + row * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE / 5

                canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill='brown', tags="wall")

def move_pawn(row, col):
    global possible_moves_for_turn
    global possible_moves_highlighted
    global possible_wall_placement_highlighted
    global possible_wall_placements

    if possible_wall_placement_highlighted:
        return

    if ((row, col) == player_1["pos"]):
    
        if possible_moves_highlighted == True:
            canvas.delete("possible_moves")
            possible_moves_highlighted = False
            possible_moves_for_turn = []

            return
        
        possible_moves_for_turn = determine_next_possible_move(row, col)
        draw_possible_grids(possible_moves_for_turn)
        possible_moves_highlighted = True
        possible_wall_placement_highlighted = False
        possible_wall_placements = []
        canvas.delete("possible_wall_placement")

    
    if possible_moves_highlighted == True and (row, col) in possible_moves_for_turn:
        canvas.delete("pawn-"+player_1["color"])
        draw_pawn(row, col, player_1["color"])
        player_1["pos"] = (row, col)
        canvas.delete("possible_moves")
        possible_moves_for_turn = []
        possible_moves_highlighted = False

        if player_1["pos"][0] == 0:
            print("win!")
        elif player_2["pos"][0] == BOARD_SIZE - 1:
            print("player 2 win!")



def determine_next_possible_move(row, col):
    possible_moves = []

    up = next_possible_cell_by_direction(row, col, "up")
    down = next_possible_cell_by_direction(row, col, "down")
    left = next_possible_cell_by_direction(row, col, "left")
    right = next_possible_cell_by_direction(row, col, "right")

    if up != None:
        possible_moves.append(up)

    if down != None:
        possible_moves.append(down)

    if left != None:
        possible_moves.append(left)

    if right != None:
        possible_moves.append(right)

    return possible_moves

def next_possible_cell_by_direction(row, col, direction):
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

    if player_2["pos"] == target_direction:
        next_move = better_cell
        if is_within_bounds(next_move):
            return next_move
        else:
            return None
        
    if not is_within_bounds(target_direction) or is_blocked_by_wall((row, col), target_direction):
       return None

    return target_direction

def get_wall_for_cell_by_direction(cell, direction="horizontal"):
    index = None

    if direction == "horizontal":
        index = next(
            (i for i, wall in enumerate(walls_built) if cell in wall and is_position_horizontal(wall)), 
            None
        )
    elif direction == "vertical":
        index = next(
            (i for i, wall in enumerate(walls_built) if cell in wall and is_position_vertical(wall)), 
            None
        )
    else:
        return None
    
    if index == None:
        return None

    return walls_built[index]

def is_blocked_by_wall(current_cell, target_cell):
    vertical_movement = is_position_vertical([current_cell, target_cell])
    horizontal_movement = is_position_horizontal([current_cell, target_cell])

    target_cell_wall_vertical = get_wall_for_cell_by_direction(target_cell, "vertical")
    target_cell_wall_horizontal = get_wall_for_cell_by_direction(target_cell, "horizontal")
    
    current_cell_wall_vertical = get_wall_for_cell_by_direction(current_cell, "vertical")
    current_cell_wall_horizontal = get_wall_for_cell_by_direction(current_cell, "horizontal")

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


def is_within_bounds(cell):
    row, col = cell

    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

def draw_possible_grids(possible_moves, tags="possible_moves"):
    for move in possible_moves:
        row, col = move[0], move[1]
        x0 = MARGIN + col * CELL_SIZE
        y0 = MARGIN + row * CELL_SIZE
        x1 = x0 + CELL_SIZE
        y1 = y0 + CELL_SIZE

        canvas.create_rectangle(x0, y0, x1, y1, outline='green', width=3, tags=tags)

if __name__ == '__main__':
    canvas.bind("<Button-1>", on_click)
    canvas.bind("<Control-Button-1>", on_right_click)
    draw_board()