def place(array):
	for i in array:
		print(" ".join(i))
		
def addCounter(player, col, grid):
	row = 8
	while row >= 0:
		if grid[row][col] == "B":
			grid[row][col] = player
			return place(grid)
		elif grid[row][col] != "B":
			row -=1
		else:
			return "Error"
			
def checkRow(player, col, row, grid):
    directions = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    colorCount = 0
    for offsetx, offsety in directions:
        checkRow = row + offsetx
        checkCol = col + offsety
        if checkRow >=0 and checkRow <= 9 and checkCol >=0 and checkCol <=9:
            if grid[checkRow][checkCol] == player:
                colorCount += 1
            return colorCount
        
def validation(player, col):
        if player != "R" or player != "Y" or col < 0 or col > 6:
            return "Please enter a valid input."
        return True
        

			


def connect4():
    grid = [["B" for row in range(6)] for i in range(9)]
    place(grid)
	
    while True:
        player = input("Enter a R or Y: ").upper()
        player_col = int(input("Enter column between 0 and 6: "))

        if validation(player, player_col) != True:
              print("Please enter a valid input.")
        break
        

