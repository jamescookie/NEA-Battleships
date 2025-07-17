#Imports
import random

#Global variables
gridSize = 6
empty = "E"

#Subroutine to create the grid and place the ships randomly
def grid():
    newGrid = [['E' for i in range(gridSize)] for i in range(gridSize)]
    placingShips(newGrid)
    return newGrid

def placingShips(grid):
    #Randomizing the place for the ship
    yAxis = random.randint(0,gridSize-1)
    xAxis = random.randint(0,gridSize//2)
    
    #Placing where the ship will go
    for i in range(gridSize//2):
        grid[yAxis][xAxis] = 's'
        xAxis += 1

#Locating the position of the ships using a search algorithm
def findingShips(grid):
    spotsArray = []
    yAxis = 0
    xAxis = 0
    for yAxis in range(gridSize):
        for xAxis in range(gridSize):
            if grid[yAxis][xAxis] == 's':
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
