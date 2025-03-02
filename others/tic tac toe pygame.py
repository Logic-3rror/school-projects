import pygame as py
import random

# Initialize Pygame
py.init()

# Screen resolution
WIDTH, HEIGHT = 1200, 800
B_W, B_H = 600, 600
BOARD_SIZE = 600
BOX_SIZE = 200
X = (WIDTH - BOARD_SIZE) // 2        #top left of grid
Y = (HEIGHT - BOARD_SIZE) // 2          


screen = py.display.set_mode((WIDTH, HEIGHT))

# Colors
white = (255, 255, 255)
colour = (250, 170, 170)
orange = (255, 165, 0)
pink = (211, 111, 231)
txt_colour = (255, 255, 255)
bg_colour = (30, 144, 255)

font = py.font.SysFont("corbel", 70)
button_font = py.font.SysFont("Corbel", 30)


def draw_grid():
    for i in range(1,3):
		# vertical lines
        py.draw.line(screen, white, (X, Y + i * BOX_SIZE), (X + BOARD_SIZE, Y + i * BOX_SIZE), 5) 
        
        # horizontal lines
        py.draw.line(screen, white, (X + i * BOX_SIZE, Y), (X + i * BOX_SIZE, Y + BOARD_SIZE), 5) 

   


def draw_button(screen, location, size, text, mouse, events):
    button_rect = py.Rect(location[0], location[1], size[0], size[1])

    # Check for hover
    if button_rect.collidepoint(mouse):
        py.draw.rect(screen, colour, button_rect)
    else:
        py.draw.rect(screen, orange, button_rect)

    # Draw button text
    text_surface = button_font.render(text, True, txt_colour)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    # Check for click
    for event in events:
        if event.type == py.MOUSEBUTTONDOWN and button_rect.collidepoint(mouse):
            return True
    return False


def grid_pos(pos):
    x, y = pos
    
    #checks if x and y are within the box
    if X <= x < X + BOARD_SIZE and Y <= y < Y + BOARD_SIZE:
        row = (y - Y) // BOX_SIZE
        col = (x - X) // BOX_SIZE
        return row, col
    else:
        return False



def find_box_center(row, col):
	#finds the box
    box_x = X + (col * BOX_SIZE)
    box_y = Y + (row * BOX_SIZE)

    # Calculate the center of the box
    center_x = (box_x + BOX_SIZE) // 2
    center_y = (box_y + BOX_SIZE) // 2

    return center_x, center_y


def draw_x(x, y):
    py.draw.line(screen, (255, 255, 255), (x - 65, y - 65), #  top left to bottom right
                 (x + 65, y + 65), 7)						
                 
    py.draw.line(screen, (255, 255, 255), (x - 65, y + 65), # top right to bottom left
                 (x + 65, y - 65), 7)
    

def win(array, shape):
    for row in range(len(array)):
        if all(array[row][col] == shape for col in range(len(array))):  # checks 3 in a row
            return row, "row"

    for col in range(len(array)):
        if all(array[row][col] == shape for row in range(len(array))):  # 3 in a row col
            return col, "col"

    if all(array[i][i] == shape for i in range(3)):
        return None, "diag"
    elif all(array[i][2 - i] == shape for i in range(3)):  #3 in a row diagonal
        return None, "n_diag" 

    return False


def draw_win_line(win_result):
    index, type_ = win_result
    if type_ == "diag":
        py.draw.line(screen,pink,(X,Y),(900,700),10)
    elif type_ == "n_diag":
        py.draw.line(screen,pink, (900,100), (300,700), 10)
    elif type_ == "row":
        py.draw.line(screen, pink, (X, Y + index * BOX_SIZE + 100 ), (X + BOARD_SIZE, Y + index * BOX_SIZE+ 100), 5)
    elif type_ == "col":
        py.draw.line(screen, pink, (X + index *  BOX_SIZE + 100, Y), (X + index * BOX_SIZE + 100, Y + BOARD_SIZE), 5)

    #py.display.update()



def emptySpaces(grid):
    empty = 0
    for i in grid:
        for j in i:
            if j == " ":
                empty += 1
    return empty


def ai(grid, ai_shape):
    coor = []
    for row, i in enumerate(grid):
        for col, j in enumerate(i):  # nested loop 2d array
            if j == " ":  # checks if empty space
                coor.append([row, col])  # updates array with index
    row, col = random.choice(coor)
    grid[row][col] = ai_shape
    return grid


def medium(grid, ai_shape, user_shape):
    coor = []
    for row in range(3):
        for col in range(3):
            if grid[row][col] == " ":
                grid[row][col] = ai_shape  # temp replaces players shape
                if win(grid, ai_shape):  # returns True if wins
                    coor.append([row, col])
                grid[row][col] = " "
    if coor:
        row, col = random.choice(coor)
        grid[row][col] = ai_shape
        return grid
    else:
        coor = []
        for row in range(3):
            for col in range(3):
                if grid[row][col] == " ":
                    grid[row][col] = user_shape  # temp replaces players shape
                    if win(grid, user_shape):  # returns True if wins
                        coor.append([row, col])
                    grid[row][col] = " "

                    # checks if there are any coor in the array
        if coor:
            row, col = random.choice(coor)
            grid[row][col] = ai_shape
            return grid
        else:
            return ai(grid, ai_shape)


def impossible():
    while True:
        mouse = py.mouse.get_pos()  # Get mouse position
        events = py.event.get()  # Get all events
        for event in events:
            if event.type == py.QUIT:
                quit()
        
            screen.fill(bg_colour)
            # Draw the title
            title_surface = font.render("Pay £25.68 :)", True, white)
            title_rect = title_surface.get_rect(center=((WIDTH // 2), 400))
            screen.blit(title_surface, title_rect)

            if draw_button(screen, (900, 650), (200, 100), "back", mouse, events):
                return ai_difficulty()
                
            py.display.update()


def ai_difficulty():
    running = True
    while running:
        mouse = py.mouse.get_pos()
        events = py.event.get()

        screen.fill(bg_colour)  # Ensure screen is cleared before drawing

        title_surface = font.render("Choose difficulty", True, white)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        draw_button(screen, (500, 200), (200, 100), "noob", mouse, events)
        draw_button(screen, (500, 400), (200, 100), "medium", mouse, events)
        draw_button(screen, (500, 600), (200, 100), "impossible???", mouse, events)
        draw_button(screen, (900, 650), (200, 100), "back", mouse, events)

        py.display.update()  # Update display after drawing buttons

        # Update display after drawing buttons

        for event in events:
            if event.type == py.QUIT:
                quit()
                
            if event.type == py.MOUSEBUTTONDOWN:
                if draw_button(screen, (500, 200), (200, 100), "noob", mouse, events):
                    return "easy"
                elif draw_button(screen, (500, 400), (200, 100), "medium", mouse, events):
                    return "medium"
                elif draw_button(screen, (500, 600), (200, 100), "impossible???", mouse, events):
                    impossible()
                if draw_button(screen, (900, 650), (200, 100), "back", mouse, events):
                    game_mode = menu()
                    main(game_mode)

            py.display.update()



def menu():
    default = "X"
    while True:
        mouse = py.mouse.get_pos()  # Get mouse position
        events = py.event.get()  # Get all events
        for event in events:
            if event.type == py.QUIT:
                quit()
        # Fill the screen with background color

        screen.fill(bg_colour)
        # Draw the title
        title_surface = font.render("Tic Tac Toe", True, white)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # Draw "Quit" button
        if draw_button(screen, (500, 600), (200, 100), "Quit", mouse, events):
            quit()
        # Draw "Player vs AI" button
        if draw_button(screen, (500, 400), (200, 100), "player vs AI", mouse, events):
            screen.fill(bg_colour)
            py.display.update()
            return "ai", default

        # Draw "Player vs Player" button
        if draw_button(screen, (500, 200), (200, 100), "player vs player", mouse, events):
            # Clear screen after selection
            screen.fill(bg_colour)
            py.display.update()
            return "pvp", default
        
        # choose X or O button
        if draw_button(screen, (880, 200), (200, 100), default, mouse, events):
            if default == "X":
                default = "O"
            else:
                default = "X"
            screen.fill(bg_colour)
            py.display.update()

        # Update the display
        py.display.update()


def main(gamemode):
    state_grid = [[" " for i in range(3)] for i in range(3)]
    mode, turn = gamemode
    shape = turn
    difficulty = None
    game_over = False
    match_ = ""

    # Handle AI difficulty selection before entering the game loop
    if mode == "ai":
        difficulty = ai_difficulty()
        if difficulty is None:  # Exit if "impossible???" or invalid choice
            return
        
        if shape == "X":
            ai_turn = "O"
        else:
            ai_turn = "X"

        # Clear screen and re-draw the grid after difficulty selection
        screen.fill(bg_colour)
        draw_grid()
        py.display.update()

    while True:
        mouse = py.mouse.get_pos()
        events = py.event.get()
        screen.fill(bg_colour)
        draw_grid()

        # Draw existing moves

        for row in range(3):
            for col in range(3):
                if state_grid[row][col] == "O":
                    center_x, center_y = find_box_center(row, col)
                    py.draw.circle(screen, white, (center_x, center_y), 70, 5)
                elif state_grid[row][col] == "X":
                    center_x, center_y = find_box_center(row, col)
                    draw_x(center_x, center_y)

        # Handle events
        for event in events:
            if event.type == py.QUIT:
                quit()


            if not game_over:
                if mode == "pvp":
                    if event.type == py.MOUSEBUTTONDOWN:
                        mouse = event.pos
                        grid_pos_result = grid_pos(mouse)
                        if grid_pos_result:
                            row, col = grid_pos_result
                            if state_grid[row][col] == " ":
                                state_grid[row][col] = shape
                                if win(state_grid, shape):
                                    match_ = f"{shape} WINS!"
                                    game_over = True
                                elif emptySpaces(state_grid) == 0:
                                    match_ = "DRAW"
                                    game_over = True

                                if not game_over:
                                    if shape == "X":
                                        shape = "O"
                                    else:
                                        shape = "X"

                elif mode == "ai":
                    #shape = turn
                    if shape == turn:
                        if event.type == py.MOUSEBUTTONDOWN:
                            mouse = event.pos
                            grid_pos_result = grid_pos(mouse)
                            if grid_pos_result:
                                row, col = grid_pos_result
                                if state_grid[row][col] == " ":
                                    state_grid[row][col] = shape
                                    if win(state_grid, shape):
                                        match_ = "PLAYER WINS!"
                                        game_over = True
                                    elif emptySpaces(state_grid) == 0:
                                        match_ = "DRAW"
                                        game_over = True
                                    else:
                                        shape = ai_turn

                    elif shape == ai_turn:

                        py.time.delay(500)

                        if difficulty == "easy":
                            state_grid = ai(state_grid, shape)
                        elif difficulty == "medium":
                            state_grid = medium(state_grid, shape, turn)

                        if win(state_grid, shape):
                            match_ = "AI WINS!"
                            game_over = True
                        elif emptySpaces(state_grid) == 0:
                            match_ = "DRAW"
                            game_over = True
                        else:
                            shape = turn 
    

        if game_over:
            if match_ == "DRAW":
                title_surface = font.render(match_, True, white)
                title_rect = title_surface.get_rect(center=(WIDTH // 2, 80))
                screen.blit(title_surface, title_rect)
            else:
                win_result = win(state_grid, shape)
                if win_result != False:  # Make sure win_result is not False 
                    draw_win_line(win_result)

                title_surface = font.render(match_, True, white)
                title_rect = title_surface.get_rect(center=(WIDTH // 2, 80))
                screen.blit(title_surface, title_rect)

            # Draw "back" button
            if draw_button(screen, (900, 650), (200, 100), "back", mouse, events):
                game_mode = menu()
                main(game_mode)

        py.display.update()


game_mode = menu()
main(game_mode)
