#Importing the grid file from gameplay
from gameplay import grid
import random

def robotChecking(userGrid, foundGame):
    return robotShooting(userGrid, foundGame)

def robotShooting(userGrid, foundGame):

    #While the player is getting an advantage to try and win
    while foundGame.handicap > 0:
        for yAxis in range(grid.gridSize):
            for xAxis in range(grid.gridSize):
                if str(userGrid[yAxis][xAxis]) == "E":
                    foundGame.handicap = foundGame.handicap - 1
                    return grid.coordsToGridReference(xAxis, yAxis)

    #Shoots every unit the player has
    for yAxis in range(grid.gridSize):
        for xAxis in range(grid.gridSize):
            if str(userGrid[yAxis][xAxis])[0] != "E" and str(userGrid[yAxis][xAxis])[-4:] != "_hit"and str(userGrid[yAxis][xAxis])[-5:] != "_sunk":
                return grid.coordsToGridReference(xAxis, yAxis)

def handicap(result, foundGame, randomizer):

    if randomizer == False:
        try:
            foundGame.handicap = int(result)
        except:
            foundGame.handicap = 0
            print("invalid input =", foundGame.handicap)

        if foundGame.handicap < 0 or foundGame.handicap > 50:
            foundGame.handicap = 0
            print("out of range input =", foundGame.handicap)
        
        print("valid =", foundGame.handicap)
    
    else:
        try:
            foundGame.handicap = int(result)
            print("random but set =", foundGame.handicap)
        except:
            number = random.randint(0, 50)
            foundGame.handicap = number
            print("randomized =", foundGame.handicap)
