#Imports
import random

#Global variables
gridSize = 6
empty = "E"

#Creates the grid layouts for mine and my opponent
opponentsGrid = [['E' for i in range(gridSize)] for i in range(gridSize)]
myGrid = [['E' for i in range(gridSize)] for i in range(gridSize)]

def placingShips(grid):
    #Randomizing the place for the ship
    randomInt1 = random.randint(0,gridSize-1)
    randomInt2 = random.randint(0,gridSize//2)

    #creating the location array for the ships
    opponentsSpotsArray = []
    
    #Placing where the ship will go
    for i in range(gridSize//2):
        grid[randomInt1][randomInt2] = 's'

        #Setting the letter and number associated with the ships location to the array
        randomLetter1 = chr(ord('A') + randomInt2 - 1)
        opponentsSpotsArray.append([str(chr(ord('A') + randomInt2)) + str(randomInt1 + 1)])
        randomInt2 += 1
    return opponentsSpotsArray


#Function for printing all the letters on the grid in python
def creatingGrid(grid):
    for row in grid:
        for spot in row:
            if spot is empty:
                print(empty, end=" ")
            else:
                print(f"{spot:1}", end=" ")
        print()

#Determining whether the submitted button presson on java is the location of the ship
def hitOrMiss(location):
    if location == opponentsSpots[0][0] or location == opponentsSpots[1][0] or location == opponentsSpots[2][0]:
        return True
    else:
        return False


#Making the array for the location of the opponents ships available for the hit or miss subroutine
opponentsSpots = placingShips(opponentsGrid)
mySpots = placingShips(myGrid)

