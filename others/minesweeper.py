#yan
import random 

grid = [[0 for n in range(10)] for i in range(10)]
placed = 0

def place(array):
    return "\n".join(" ".join(map(str, row)) for row in array)

def checkMines(row, col):
    directions = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    minecount = 0
    for offsetx, offsety in directions:
        checkRow = row + offsetx
        checkCol = col + offsety
        if 0 <= checkRow < 10 and 0 <= checkCol < 10:
            if grid[checkRow][checkCol] == -1:
                minecount += 1
            return minecount


while placed < 5:
    mine_row = random.randint(0,9)
    mine_col = random.randint(0,9)
    grid[mine_row][mine_col] = "-1"
    if grid[mine_row][mine_col] == -1:
        placed = 0
    placed +=1

for row in grid:
    for col in range(len(row)):
        if row[col] == -1:
            row[col] = 0  

print(place(grid))


rounds = 0
valid = False
while rounds < 10: 

    user_row, user_col = map(int, input("Enter a row and column (0-9) - ").split())

    while not (0 <= user_row < 10 and 0 <= user_col < 10):
        print("Enter a valid input between 0 and 9")
        user_row, user_col = map(int, input("Enter a row and column (0-9) - ").split())

    if grid[user_row][user_col] == -1:
        print("Game Over.")
        break 

    grid[user_row][user_col] = checkMines(user_row, user_col)
    print(place(grid))

    rounds += 1


if rounds >= 10:
    print("Well Done! You won.")

