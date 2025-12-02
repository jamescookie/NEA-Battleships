#Imports
import random
#Global variables
gridSize = 10
empty = "E"


#Subroutine to create the grid and place the ships randomly
def grid(units):
    newGrid = [['E' for i in range(gridSize)] for j in range(gridSize)]
    for i in range(len(units)):
        checkingShips(newGrid, units[i])
    #Prints the grid and location of all the ships for ease of debugging
    printingGrid(newGrid)
    return newGrid


#This entire subroutine is to check and place ships in the grid created
def checkingShips(grid, troop):
    #These are collecting the data of the ships in the units folder
    type = troop[0]
    width = troop[1]
    length = troop[2]
    check = False
    #This is to be used by the program to determine which direction the ship will be placed in, but also reset for every new ship
    directionArray = [["Y", -1],
                      ["X", 1],
                      ["Y", 1],
                      ["X", -1]]

    while check == False:
        locationCheck = False
        #Checking if the directionArray is full or empty
        if len(directionArray) == 4 or len(directionArray) == 0:
            directionArray = [["Y", -1],
                            ["X", 1],
                            ["Y", 1],
                            ["X", -1]]
            #While loop to keep creating new starting coordinates if the ones created are inaccurate (on top of another ship)
            while locationCheck == False:
                #Creating the coordinates for the ship
                yAxis = random.randint(0,gridSize-1)
                xAxis = random.randint(0,gridSize-1)
                #Logging the location of the original coordinates because the yAxis and xAsis are going to get changed
                
                coordinates = [yAxis, xAxis]
                #locationCheck will come back true or false
                locationCheck = canIPlaceAUnitHere(yAxis, xAxis, grid)

        #This is to make sure that the random integer next won't break when there's only one item in the array
        if len(directionArray) == 1:
            index = 0    
        else:    
            #Randomly selecting the number connected to the direction (0-North, 1-East)
            index = random.randint(0, len(directionArray)-1)
        
        #Sets value and checkingValue to the value of the specific direction it chose
        value = directionArray[index][1]
        checkingValue = directionArray[index][1]
        #Removes the axis from the list and sets it as the variable 'axis'
        axis = directionArray.pop(index)[0]
        
        checkingCoordinates = [yAxis, xAxis]
        #This if statement will only run if the ship, currently being chosen is only 1 square wide
        #This section is only for checking the entire ship can be placed in the designated area
        if width == 1:
            #This will keep running for the entire length of the ship minus 1
            for j in range (length-1):
                #This makes the next coordinates of the ship to be in the direction selected
                checkingCoordinates = actualPlacingShips(checkingCoordinates, axis, type, grid, value, 0, 1, False)
                if canIPlaceAUnitHere(checkingCoordinates[0], checkingCoordinates[1], grid) == False:
                    break

        #The only difference to this is that it's for ships that are larger than 1 square wide
        else:
            for i in range (width):
                for j in range(length-1):
                    checkingCoordinates = actualPlacingShips(checkingCoordinates, axis, type, grid, checkingValue, 0, 1, False)
                    if canIPlaceAUnitHere(checkingCoordinates[0], checkingCoordinates[1], grid) == False:
                        break
                if canIPlaceAUnitHere(checkingCoordinates[0], checkingCoordinates[1], grid) == False:
                    break

                #This will make the ship turn direction after it completes the first run through and go back the other way along an axis directly next to the first one
                if i != width-1:
                    checkingCoordinates = actualPlacingShips(checkingCoordinates, axis, type, grid, checkingValue, 1, 0, False)
                    if canIPlaceAUnitHere(checkingCoordinates[0], checkingCoordinates[1], grid) == False:
                        break
                    #This makes the ship go the opposite way that it just went
                    checkingValue = -checkingValue
            if canIPlaceAUnitHere(checkingCoordinates[0], checkingCoordinates[1], grid) == False:
                continue  
        if canIPlaceAUnitHere(checkingCoordinates[0], checkingCoordinates[1], grid) == True:
            check = True

    #The first instance of actually setting a ship on the grid after all checks have been completed
    grid[coordinates[0]][coordinates[1]] = type
    
    #This section is the exact same as the previous but without checking whether it can fit because it already knows it can
    if width == 1:
        for j in range (length-1):
            coordinates = actualPlacingShips(coordinates, axis, type, grid, value, 0, 1, True)
    else:
        for i in range (width):
            for j in range(length-1):
                coordinates = actualPlacingShips(coordinates, axis, type, grid, value, 0, 1, True)
            if i != width-1:
                coordinates = actualPlacingShips(coordinates, axis, type, grid, value, 1, 0, True)
                value = -value


def actualPlacingShips(coordinates, axis, type, grid, value, num1, num2, placing):
    if axis == "Y":
        #Increments the coordinates of the ship by one in either the Y axis or X axis
        coordinates[num1] += value
    else:
        coordinates[num2] += value
    if placing == True:
        #This is setting the position of 1 part of a ship
        grid[coordinates[0]][coordinates[1]] = type
    return coordinates


def canIPlaceAUnitHere(y, x, grid):
    #This makes sure the x coordinate and y coordinate is inside the grid and not lower than 1
    #It also makes sure that the coordinate chosen is not already occupied by another ship
    if x < gridSize and x >= 0 and y < gridSize and y >= 0 and grid[y][x] == empty:
        return True
    else:
        return False


#Locating the position of the ships using a search algorithm
def findingShips(grid, allShips, slot):
    spotsArray = []
    for yAxis in range(gridSize):
        for xAxis in range(gridSize):
            #This makes it so that either the spots array is collecting every coordinate of the ships or just a specific ship
            if allShips == True:
                if grid[yAxis][xAxis] != slot:
                    #Once the location of A ship is found, label the position with coordinates (A1, C5, E2)
                    spotsArray.append(str(chr(ord('A') + xAxis)) + str(yAxis + 1))   
            else:
                if grid[yAxis][xAxis] == slot:
                    #Once the location of THE ship is found, label the position with coordinates (A1, C5, E2)
                    spotsArray.append(str(chr(ord('A') + xAxis)) + str(yAxis + 1))         
    return spotsArray


#Changes (0, 2) or (8, 5), for example, into (A, 3) or (I, 6) respectively
def coordsToGridReference(xAxis,yAxis):
    x = str(chr(ord('A') + xAxis))
    y = str(yAxis + 1)
    #Return a string of just A3 or I6
    return str(x + y)


#Changes (A, 3) or (I, 6), for example, into (0, 2) or (8, 5) respectively
def gridReference(grid, reference, new):
    x = int(ord(reference[0])) - 65
    y = int(reference[1:]) - 1
    #Just returns what the message in the coordinates is
    if new == None:
        return grid[y][x]
    #Changes the coordinates of the grid into the new message
    grid[y][x] = new
    

#Function for printing all the letters on the grid in python
#It's not used in the main program but is useful to have when debugging
def printingGrid(grid):
    #This is just to space out the grid printed, so it's not too confusing
    print("--------------------------------------------------------------------------------------------")
    #Creates the letters at the top of the board
    for i in range(len(grid[0])):
        print(chr(ord('A') + int(i)), end=" ")
    #Prints an extra line
    print("\n")
    #For every row in the grid (10) and every spot in the rows (10)
    for row in grid:
        for spot in row:
            #If the spot is empty, then it prints an "E" with a space to seperate the E's
            if spot is empty:
                print(empty, end=" ")
            else:
                #Prints the unit in the spot with a space
                print(f"{spot:1}", end=" ")
        print()
    #Used to create a new line to print on
    print()
    #Creates the letters at the bottom of the board
    for i in range(len(grid[0])):
        print(chr(ord('A') + int(i)), end=" ")
    print("\n--------------------------------------------------------------------------------------------")
