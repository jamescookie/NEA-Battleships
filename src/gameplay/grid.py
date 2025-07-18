#Imports
import random

#Global variables
gridSize = 10
empty = "E"

#Subroutine to create the grid and place the ships randomly
def grid(units):
    #print(units)
    newGrid = [['E' for i in range(gridSize)] for i in range(gridSize)]
    for i in range(len(units)):
        placingShips(newGrid, units[i])
    #print(newGrid)
    return newGrid

def placingShips(grid, troop):
    #print("HI")
    type = troop[0]
    width = troop[1]
    length = troop[2]
    check = False
    directionArray = ["north", "east", "south", "west"]

    while check == False:
        locationCheck = False
        if len(directionArray) == 4 or len(directionArray) == 0:
            directionArray = ["north", "east", "south", "west"]
            while locationCheck == False:
                yAxis = random.randint(0,gridSize-1)
                xAxis = random.randint(0,gridSize-1)
                startingY = yAxis
                startingX = xAxis
                locationCheck = canIPlaceAUnitHere(xAxis, yAxis, grid)

        if len(directionArray) == 1:
            index = 0    
        else:    
            index = random.randint(0, len(directionArray)-1)
        direction = directionArray.pop(index)
        
        if direction == "north":
            if compassDirections(direction, 1, width, length, xAxis, yAxis, grid) == True:
                check = True
            else:
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


    one = 1
    if width == 1:
        for j in range (length):
            grid[startingY][startingX] = type
            #print("width: ", width, "length: ", length, "startingX: ", startingX,"startingY: ", startingY, "i: ", i, "j: ", j)
            if direction == "north":
                startingY += 1
            elif direction == "east":
                startingX += 1
            elif direction == "south":
                startingY -= 1
            elif direction == "west":
                startingX -= 1
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
            if i != width-1:
                if direction == "north":
                    startingX += one
                elif direction == "east":
                    startingY += one
                elif direction == "south":
                    startingX -= one
                elif direction == "west":
                    startingY -= one          
                one = -one


def compassDirections (direction, value, width, length, x, y, grid):
    if width == 1:
        for j in range(length-1):
                #print("width: ", width, "length: ", length, "x: ", x,"y: ", y, "i: ", i, "j: ", j)
            if direction == "north" or direction == "south":
                y += value
            else:
                x += value
            if canIPlaceAUnitHere(x, y, grid) == False:
                return False          
    else:
        for i in range (width):
            for j in range(length-1):
                #print("width: ", width, "length: ", length, "x: ", x,"y: ", y, "i: ", i, "j: ", j)
                if direction == "north" or direction == "south":
                    y += value
                else:
                    x += value
                if canIPlaceAUnitHere(x, y, grid) == False:
                    return False
            if i != width-1:
                if direction == "north" or direction == "south":
                    x += value
                else:
                    y += value
                if canIPlaceAUnitHere(x, y, grid) == False:
                    return False
                value = -value
    return True


def canIPlaceAUnitHere(x, y, grid):
    #print(gridSize, x, y)
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
def printingGrid(grid):
    for row in grid:
        for spot in row:
            if spot is empty:
                print(empty, end=" ")
            else:
                print(f"{spot:1}", end=" ")
        print()
