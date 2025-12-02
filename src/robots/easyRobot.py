#Importing random and the grid file from gameplay
import random
from gameplay import grid

def robotShooting(userGrid):
    #Randomly chooses an x and y coordinate to shoot
    yAxis = random.randint(0,grid.gridSize-1)
    xAxis = random.randint(0,grid.gridSize-1)
    #This sends the grid reference the user's grid, the (Letter, Number) version of coordinates and that it's not changing the grid
    #'type' is then set to whatever is in the coordinates
    type = grid.gridReference(userGrid, grid.coordsToGridReference(xAxis, yAxis), None)
    #Checks to see that the last characters of the spot chosen has not been hit or missed already
    #Essentially makes sure that the robot can't shoot in the same place twice
    while str(type)[-4:] == "_hit" or str(type)[-5:] == "_miss":
        #Resets the x and y coordinates until the location is acceptable
        yAxis = random.randint(0,grid.gridSize-1)
        xAxis = random.randint(0,grid.gridSize-1)
        type = grid.gridReference(userGrid, grid.coordsToGridReference(xAxis, yAxis), None)

    #Makes sure to return the (Letter, Number) version of coordinates (Or grid reference)
    return grid.coordsToGridReference(xAxis, yAxis)
