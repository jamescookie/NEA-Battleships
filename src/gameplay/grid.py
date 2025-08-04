#Imports
import random

#Global variables
gridSize = 10
empty = "E"

#Subroutine to create the grid and place the ships randomly
def grid(units):
    newGrid = [['E' for i in range(gridSize)] for i in range(gridSize)]
    for i in range(len(units)):
        placingShips(newGrid, units[i])
    return newGrid

#This entire subroutine is to check and place ships in the grid created
def placingShips(grid, troop):
    #These are collecting the data of the ships in the units folder
    type = troop[0]
    width = troop[1]
    length = troop[2]
    check = False
    #This is to be used by the program to determine which direction the ship will be placed in, but also reset for every new ship
    directionArray = ["north", "east", "south", "west"]

    while check == False:
        locationCheck = False
        #Checking if the directionArray is full or empty
        if len(directionArray) == 4 or len(directionArray) == 0:
            directionArray = ["north", "east", "south", "west"]
            #While loop to keep creating new starting coordinates if the ones created are inaccurate (on top of another ship)
            while locationCheck == False:
                #Creating the coordinates for the ship
                yAxis = random.randint(0,gridSize-1)
                xAxis = random.randint(0,gridSize-1)
                #Logging the location of the original coordinates because the yAxis and xAsis are going to get changed
                startingY = yAxis
                startingX = xAxis
                #locationCheck will come back true or false
                locationCheck = canIPlaceAUnitHere(xAxis, yAxis, grid)

        if len(directionArray) == 1:
            index = 0    
        else:    
            #Randomly selecting the number connected to the direction (0-North, 1-East)
            index = random.randint(0, len(directionArray)-1)
        #Removes the direction from the list and sets it as the variable 'direction'
        direction = directionArray.pop(index)
        
        #The next 4 if statements are to ask the function 'compassDirections' if the entire ship can fit in the grid going in this specific direction
        if direction == "north":
            if compassDirections(direction, 1, width, length, xAxis, yAxis, grid) == True:
                check = True
            else:
                #This continue means it won't break out of the while loop, but will continue to the first if statement in the while loop
                continue       
        
        elif direction == "east":
            if compassDirections(direction, 1, width, length, xAxis, yAxis, grid) == True:
                check = True
            else:
                continue

        elif direction == "south":
            if compassDirections(direction, -1, width, length, xAxis, yAxis, grid) == True:
                check = True
            else:            
                continue

        elif direction == "west":
            if compassDirections(direction, -1, width, length, xAxis, yAxis, grid) == True:
                check = True
            else: 
                continue

    #This can only start once the entire ship has been checked that it can fit in the grid, without colliding
    #This 'one' is to allow it to become negative
    one = 1
    #This if statement will only run if the ship, currently being chosen is only 1 square wide
    if width == 1:
        #This will keep running for the entire length of the ship
        for j in range (length):
            #This sets the starting location of the ship to the type of ship it is (like submarine)
            grid[startingY][startingX] = type
            #This is the only point where the startingY and X will change because the program now knows that it can fit which direction it wants to go
            if direction == "north":
                startingY += 1
            elif direction == "east":
                startingX += 1
            elif direction == "south":
                startingY -= 1
            elif direction == "west":
                startingX -= 1
    #The only difference to this is that it's for ships that are larger than 1 square wide
    else:
        for i in range (width):
            for j in range(length-1):
                grid[startingY][startingX] = type
                if direction == "north":
                    startingY += one
                elif direction == "east":
                    startingX += one
                elif direction == "south":
                    startingY -= one
                elif direction == "west":
                    startingX -= one
            grid[startingY][startingX] = type
            #This will make the ship turns direction after it completes the first run through and go back the other way along an axis directly next to the first one
            if i != width-1:
                if direction == "north":
                    startingX += one
                elif direction == "east":
                    startingY += one
                elif direction == "south":
                    startingX -= one
                elif direction == "west":
                    startingY -= one          
                #This makes the ship go the opposite way that it just went
                one = -one

#This is the function that checks whether the entire ship can be placed using that direction
def compassDirections (direction, value, width, length, x, y, grid):
    #This is for only when the ship is 1 square wide
    if width == 1:
        #This will go 1 square at a time for the length of the ship
        for j in range(length-1):
            if direction == "north" or direction == "south":
                y += value
            else:
                x += value
            #This checks whether the new spot is not occupied and inside of the grid
            if canIPlaceAUnitHere(x, y, grid) == False:
                return False          
    #This does the same but when the ship is more than 1 square wide
    else:
        for i in range (width):
            for j in range(length-1):
                if direction == "north" or direction == "south":
                    y += value
                else:
                    x += value
                if canIPlaceAUnitHere(x, y, grid) == False:
                    return False
            #This will make the ship turns direction after it completes the first run through and go back the other way along an axis directly next to the first one
            if i != width-1:
                if direction == "north" or direction == "south":
                    x += value
                else:
                    y += value
                if canIPlaceAUnitHere(x, y, grid) == False:
                    return False
                #This makes the ship go the opposite way that it just went
                value = -value
    return True


def canIPlaceAUnitHere(x, y, grid):
    #This makes sure the x coordinate and y coordinate is inside the grid and not lower than 1
    #It also makes sure that the coordinate chosen is not already occupied by another ship
    if x < gridSize and x >= 0 and y < gridSize and y >= 0 and grid[y][x] == empty:
        return True
    else:
        return False


#Locating the position of the ships using a search algorithm
def findingShips(grid):
    spotsArray = []
    yAxis = 0
    xAxis = 0
    for yAxis in range(gridSize):
        for xAxis in range(gridSize):
            if grid[yAxis][xAxis] != empty:
                #Once the location of the ship is found, label the position with coordinates (A1, C5, E2)
                spotsArray.append(str(chr(ord('A') + xAxis)) + str(yAxis + 1))
    return spotsArray



#Function for printing all the letters on the grid in python
#It's not used in the main program but is useful to have when debugging
def printingGrid(grid):
    for row in grid:
        for spot in row:
            if spot is empty:
                print(empty, end=" ")
            else:
                print(f"{spot:1}", end=" ")
        print()
