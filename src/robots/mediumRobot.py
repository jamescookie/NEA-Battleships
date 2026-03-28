#Importing random and the grid file from gameplay
import random
from gameplay import grid
from gameplay import game

def robotChecking(userGrid, foundGame):

    #If this is the first time the robot is shooting
    if len(foundGame.robotShots) == 0:
        return robotShooting(userGrid, foundGame)


    #Collect the last shot that the robot took
    lastShot = [str(foundGame.robotShots[-1][0]), str(foundGame.robotShots[-1][1:])]

    #Changing an array into a string E.g. ['D', '5'] becomes 'D5'
    lastGridReference = lastShot[0] + lastShot[1]

    #Changing the grid reference into coordinates that python can use
    lastCoordinates = grid.gridReferenceToCoords(userGrid, lastGridReference, None, True)

    #Converts the coordinates into an array E.g. 'D5' becomes (3, 4) which then becomes [3, 4]
    lastCoordinates = [int(lastCoordinates[0]), int(lastCoordinates[1])]

    #Creates a copy of the coordinates so that when checking, the coordinates aren't changed
    checkingCoordinates = [lastCoordinates[0], lastCoordinates[1]]

    #Finds the result of the shot that was first fired (hit or miss)
    answer = grid.gridReferenceToCoords(userGrid, lastGridReference, None, False)


    #If the robot has sunk a ship
    if foundGame.userShipsSunk != 0:

        if str(answer)[-5:] == "_sunk":
            #Resets all settings that were changed when trying to locate the rest of the ship
            foundGame.robotDirection = [["Y", -1],
                                        ["X", 1],
                                        ["Y", 1],
                                        ["X", -1]]
            foundGame.robotAxis = None
            foundGame.robotValue = None

        #Makes a list for every troop that has been hit after a ship has been sunk
        notSunkArray = []
        notSunkArrayCoords = []
        for yAxis in range(grid.gridSize):
            for xAxis in range(grid.gridSize):
                if str(userGrid[yAxis][xAxis])[-4:] == "_hit":
                    notSunkArray.append(userGrid[yAxis][xAxis])
                    notSunkCoords = str(yAxis) + str(xAxis)
                    notSunkArrayCoords.append(notSunkCoords)

        #If there isn't another ship that has been hit
        if len(notSunkArray) == 0:
            return robotShooting(userGrid, foundGame)
        
        #If another ship has been hit
        else:
            for i in range (len(foundGame.robotFirstHit)):
                if len(notSunkArray) == 1:
                    if (str(foundGame.robotFirstHit[i][0]) + "_hit") == notSunkArray[0]:
                        foundGame.robotAttacking = foundGame.robotFirstHit[i][0]
                        x = int(notSunkArrayCoords[0][1])
                        y = int(notSunkArrayCoords[0][0])
                        coordinate = grid.coordsToGridReference(x, y)
                        foundGame.robotShots.append(coordinate)
                        break

                copyNotSunkArray = notSunkArray
                #Set function removes all copies of data in the array
                #If (the length of the array) is equal to (the array that has removed all duplicate data) then
                if len(notSunkArray) == len(set(copyNotSunkArray)):
                    if (str(foundGame.robotFirstHit[i][0]) + "_hit") == notSunkArray[0]:
                        foundGame.robotAttacking = foundGame.robotFirstHit[i][0]
                        x = int(notSunkArrayCoords[0][1])
                        y = int(notSunkArrayCoords[0][0])
                        coordinate = grid.coordsToGridReference(x, y)
                        foundGame.robotShots.append(coordinate)
                        break

                #If any other troop has been hit multiple times
                else:
                    if (str(foundGame.robotFirstHit[i][0]) + "_hit") == foundGame.robotAttacking:
                        x = int(foundGame.robotShots[-(len(notSunkArray))][1])
                        y = int(foundGame.robotShots[-(len(notSunkArray))][0])
                        coordinate = grid.coordsToGridReference(x, y)
                        foundGame.robotShots.append(coordinate)
                        break


    #To check if the robot has hit a troop in a row
    for i in range (len(foundGame.robotFirstHit)):
        if foundGame.robotFirstHit[i][0] == foundGame.robotAttacking:
            hitArray = []
            troop = (str(foundGame.robotFirstHit[i][0]) + "_hit")
            hitArray = grid.findingTroops(userGrid, False, troop)
            if len(hitArray) > 1:

                #Collect the last shot that the robot took
                lastShot = [str(foundGame.robotShots[-1][0]), str(foundGame.robotShots[-1][1:])]

                #Changing an array into a string E.g. ['D', '5'] becomes 'D5'
                lastGridReference = lastShot[0] + lastShot[1]

                #Changing the grid reference into coordinates that python can use
                lastCoordinates = grid.gridReferenceToCoords(userGrid, lastGridReference, None, True)

                #Converts the coordinates into an array E.g. 'D5' becomes (3, 4) which then becomes [3, 4]
                lastCoordinates = [int(lastCoordinates[0]), int(lastCoordinates[1])]

                #Creates a copy of the coordinates so that the starting position of the coordinates remains the same
                checkingCoordinates = [lastCoordinates[0], lastCoordinates[1]]

                #Finds the result of the shot that was first fired (hit or miss)
                answer = grid.gridReferenceToCoords(userGrid, lastGridReference, None, False)

                #If the last shot did not hit the troop that the robot is attacking (aka missing)
                if str(answer) != (str(foundGame.robotAttacking) + "_hit"):   
                    check = False

                    #Collect the second to last shot that the robot took
                    lastShot = [str(foundGame.robotShots[-2][0]), str(foundGame.robotShots[-2][1:])]
                    
                    #Changing an array into a string E.g. ['D', '5'] becomes 'D5'
                    lastGridReference = lastShot[0] + lastShot[1]

                    answer = grid.gridReferenceToCoords(userGrid, lastGridReference, None, False)

                    #Removes the _hit from the unit that has been hit
                    checkingAnswer = answer.split("_hit")
                    for i in range (len(foundGame.robotFirstHit)):
                        #If the unit hit is in the array
                        if checkingAnswer[0] == foundGame.robotFirstHit[i][0]:
                            #Record the coordinates of the first time that specific unit has been hit
                            coordinates = [int(foundGame.robotFirstHit[i][1][0]), int(foundGame.robotFirstHit[i][1][1])]
                            checkingCoordinates = [coordinates[0], coordinates[1]]

                    game.settingAttr(foundGame, 'robotValue', -foundGame.robotValue)
                    
                    #Finds the next coordinates the robot will be shooting at, using the axis and value randomly selected
                    nextCoordinates = grid.placingTroops(checkingCoordinates, foundGame.robotAxis, None, None, 
                                                            foundGame.robotValue, 0, 1, False)

                    while check == False:
                        #Checks if the next coordinates are still on the board
                        if grid.canIPlaceAUnitHere(nextCoordinates[1], nextCoordinates[0], userGrid, foundGame, True) == True:
                            check = True
                            break
                        else:
                            checkingCoordinates = [coordinates[0], coordinates[1]]
                            #This is to make sure that the random integer next won't break 
                            #when there's only one item in the array
                            if len(foundGame.robotDirection) == 1:
                                index = 0    
                            else:    
                                #Randomly selecting the number connected to the direction (0-North, 1-East)
                                index = random.randint(0, len(foundGame.robotDirection)-1)
                            
                            game.settingAttr(foundGame, 'robotAxis', foundGame.robotDirection[index][0])
                            game.settingAttr(foundGame, 'robotValue', foundGame.robotDirection.pop(index)[1])

                            nextCoordinates = grid.placingTroops(checkingCoordinates, foundGame.robotAxis, None, None, 
                                                                    foundGame.robotValue, 0, 1, False)
            
                    nextGridReference = grid.coordsToGridReference(nextCoordinates[0], nextCoordinates[1])
                    foundGame.robotShots.append(nextGridReference)
                    return nextGridReference

                elif str(answer)[-4:] == "_hit":

                    check = False

                    #Collect the last shot that the robot took
                    lastShot = [str(foundGame.robotShots[-1][0]), str(foundGame.robotShots[-1][1:])]

                    #Changing an array into a string E.g. ['D', '5'] becomes 'D5'
                    lastGridReference = lastShot[0] + lastShot[1]

                    #Changing the grid reference into coordinates that python can use
                    lastCoordinates = grid.gridReferenceToCoords(userGrid, lastGridReference, None, True)

                    #Converts the coordinates into an array E.g. 'D5' becomes (3, 4) which then becomes [3, 4]
                    lastCoordinates = [int(lastCoordinates[0]), int(lastCoordinates[1])]

                    #Creates a copy of the coordinates so that the starting position of the coordinates remains the same
                    checkingCoordinates = [lastCoordinates[0], lastCoordinates[1]]
                    
                    #Finds the next coordinates the robot will be shooting at, using the axis and value randomly selected
                    nextCoordinates = grid.placingTroops(checkingCoordinates, foundGame.robotAxis, None, None, 
                                                            foundGame.robotValue, 0, 1, False)

                    #Checks if the next coordinate has already been shot at or is off the board
                    if grid.canIPlaceAUnitHere(nextCoordinates[1], nextCoordinates[0], userGrid, foundGame, True) == False:

                        #Removes the _hit from the unit that has been hit
                        checkingAnswer = answer.split("_hit")
                        for i in range (len(foundGame.robotFirstHit)):
                            #If the unit hit is in the array
                            if checkingAnswer[0] == foundGame.robotFirstHit[i][0]:
                                #Record the coordinates of the first time that specific unit has been hit
                                coordinates = [int(foundGame.robotFirstHit[i][1][0]), int(foundGame.robotFirstHit[i][1][1])]
                                checkingCoordinates = [coordinates[0], coordinates[1]]


                        game.settingAttr(foundGame, 'robotValue', -foundGame.robotValue)

                        #Finds the next coordinates the robot will be shooting at, using the axis and value randomly selected
                        nextCoordinates = grid.placingTroops(checkingCoordinates, foundGame.robotAxis, None, None, 
                                                                foundGame.robotValue, 0, 1, False)

                        while check == False:
                            #Checks if the next coordinates are still on the board
                            if grid.canIPlaceAUnitHere(nextCoordinates[1], nextCoordinates[0], userGrid, foundGame, True) == True:
                                check = True
                                break
                            else:
                                checkingCoordinates = [coordinates[0], coordinates[1]]
                                #This is to make sure that the random integer next won't break 
                                #when there's only one item in the array
                                if len(foundGame.robotDirection) == 1:
                                    index = 0    
                                else:    
                                    #Randomly selecting the number connected to the direction (0-North, 1-East)
                                    index = random.randint(0, len(foundGame.robotDirection)-1)
                                
                                game.settingAttr(foundGame, 'robotAxis', foundGame.robotDirection[index][0])
                                game.settingAttr(foundGame, 'robotValue', foundGame.robotDirection.pop(index)[1])

                                nextCoordinates = grid.placingTroops(checkingCoordinates, foundGame.robotAxis, None, None, 
                                                                        foundGame.robotValue, 0, 1, False)
                
                        nextGridReference = grid.coordsToGridReference(nextCoordinates[0], nextCoordinates[1])
                        foundGame.robotShots.append(nextGridReference)
                        return nextGridReference
                    
                    else:
                        nextGridReference = grid.coordsToGridReference(nextCoordinates[0], nextCoordinates[1])
                        foundGame.robotShots.append(nextGridReference)
                        return nextGridReference


            #If any troop has only been hit once
            else:
                check = False

                #Converts the coordinates into an array E.g. 'D5' becomes (3, 4) which then becomes [3, 4]
                lastCoordinates = [int(foundGame.robotFirstHit[i][1][0]), int(foundGame.robotFirstHit[i][1][1])]

                #Creates a copy of the coordinates so that the starting position of the coordinates remains the same
                checkingCoordinates = [lastCoordinates[0], lastCoordinates[1]]

                #This is to make sure that the random integer next won't break when there's only one item in the array
                if len(foundGame.robotDirection) == 1:
                    index = 0    
                else:    
                    #Randomly selecting the number connected to the direction (0-North, 1-East)
                    index = random.randint(0, len(foundGame.robotDirection)-1)
                
                #Setting the attributes of the axis and value the robot will be shooting in next
                foundGame.robotAxis = foundGame.robotDirection[index][0]
                foundGame.robotValue = foundGame.robotDirection.pop(index)[1]

                #Finds the next coordinates the robot will be shooting at, using the axis and value randomly selected
                nextCoordinates = grid.placingTroops(checkingCoordinates, foundGame.robotAxis, 
                                                    None, None, foundGame.robotValue, 0, 1, False)

                while check == False:
                    #Checks if the next coordinates are still on the board or if it hasn't been shot there already
                    if grid.canIPlaceAUnitHere(nextCoordinates[1], nextCoordinates[0], userGrid, foundGame, 
                                            True) == True:
                        check = True
                        break
                    else:
                        checkingCoordinates = [lastCoordinates[0], lastCoordinates[1]]
                        #This is to make sure that the random integer next won't break 
                        #when there's only one item in the array
                        if len(foundGame.robotDirection) == 1:
                            index = 0    
                        else:    
                            #Randomly selecting the number connected to the direction (0-North, 1-East)
                            index = random.randint(0, len(foundGame.robotDirection)-1)
                        
                        #Setting the attributes of the axis and value the robot will be shooting in next
                        game.settingAttr(foundGame, 'robotAxis', foundGame.robotDirection[index][0])
                        game.settingAttr(foundGame, 'robotValue', foundGame.robotDirection.pop(index)[1])

                        #Finds the next coordinates the robot will be shooting at, using the axis and value randomly selected
                        nextCoordinates = grid.placingTroops(checkingCoordinates, foundGame.robotAxis, 
                                                            None, None, foundGame.robotValue, 0, 1, False)

                #Once the next shot is actually available, make the coordinates into a grid reference
                nextGridReference = grid.coordsToGridReference(nextCoordinates[0], nextCoordinates[1])

                #Adds the shot fired to the robotShots array
                foundGame.robotShots.append(nextGridReference)
                return nextGridReference


    #If the robot hasn't hit the same troop twice
    check = False

    #Collect the last shot that the robot took
    lastShot = [str(foundGame.robotShots[-1][0]), str(foundGame.robotShots[-1][1:])]

    #Changing an array into a string E.g. ['D', '5'] becomes 'D5'
    lastGridReference = lastShot[0] + lastShot[1]

    #Changing the grid reference into coordinates that python can use
    lastCoordinates = grid.gridReferenceToCoords(userGrid, lastGridReference, None, True)

    #Converts the coordinates into an array E.g. 'D5' becomes (3, 4) which then becomes [3, 4]
    lastCoordinates = [int(lastCoordinates[0]), int(lastCoordinates[1])]

    #Creates a copy of the coordinates so that the starting position of the coordinates remains the same
    checkingCoordinates = [lastCoordinates[0], lastCoordinates[1]]

    #Finds the result of the shot that was first fired (hit or miss)
    answer = grid.gridReferenceToCoords(userGrid, lastGridReference, None, False)

    if str(answer)[-5:] == "_miss":
        
        #Continues to shoot randomly if the shot missed
        return robotShooting(userGrid, foundGame)

    elif str(answer)[-4:] == "_hit":

        #Finds what troop has been hit and decides that that one will be the one the robot is attacking
        for i in range (len(foundGame.robotFirstHit)):
            if foundGame.robotFirstHit[i][1] != None:
                foundGame.robotAttacking = foundGame.robotFirstHit[i][0]


        #This is to make sure that the random integer next won't break 
        #when there's only one item in the array
        if len(foundGame.robotDirection) == 1:
            index = 0    
        else:    
            #Randomly selecting the number connected to the direction (0-North, 1-East)
            index = random.randint(0, len(foundGame.robotDirection)-1)
        
        #Setting the attributes of the axis and value the robot will be shooting in next
        foundGame.robotAxis = foundGame.robotDirection[index][0]
        foundGame.robotValue = foundGame.robotDirection.pop(index)[1]

        #Finds the next coordinates the robot will be shooting at, using the axis and value randomly selected
        nextCoordinates = grid.placingTroops(checkingCoordinates, foundGame.robotAxis, 
                                            None, None, foundGame.robotValue, 0, 1, False)

        while check == False:
            #Checks if the next coordinates are still on the board or if it hasn't been shot there already
            if grid.canIPlaceAUnitHere(nextCoordinates[1], nextCoordinates[0], userGrid, foundGame, 
                                    True) == True:
                check = True
                break
            else:
                checkingCoordinates = [lastCoordinates[0], lastCoordinates[1]]
                #This is to make sure that the random integer next won't break when there's only one item in the array
                if len(foundGame.robotDirection) == 1:
                    index = 0    
                else:    
                    #Randomly selecting the number connected to the direction (0-North, 1-East)
                    index = random.randint(0, len(foundGame.robotDirection)-1)
                
                #Setting the attributes of the axis and value the robot will be shooting in next
                game.settingAttr(foundGame, 'robotAxis', foundGame.robotDirection[index][0])
                game.settingAttr(foundGame, 'robotValue', foundGame.robotDirection.pop(index)[1])

                #Finds the next coordinates the robot will be shooting at, using the axis and value randomly selected
                nextCoordinates = grid.placingTroops(checkingCoordinates, foundGame.robotAxis, 
                                                    None, None, foundGame.robotValue, 0, 1, False)

        #Once the next shot is actually available, make the coordinates into a grid reference
        nextGridReference = grid.coordsToGridReference(nextCoordinates[0], nextCoordinates[1])

        #Adds the shot fired to the robotShots array
        foundGame.robotShots.append(nextGridReference)
        return nextGridReference



def robotShooting(userGrid, foundGame):
        #Randomly chooses an x and y coordinate to shoot
        yAxis = random.randint(0,grid.gridSize-1)
        xAxis = random.randint(0,grid.gridSize-1)
        #This sends the grid reference the user's grid, the (Letter, Number) version of coordinates 
        #and that it's not changing the grid
        #'type' is then set to whatever is in the coordinates
        type = grid.gridReferenceToCoords(userGrid, grid.coordsToGridReference(xAxis, yAxis), None, False)
        #Checks to see that the last characters of the spot chosen has not been hit or missed already
        #Essentially makes sure that the robot can't shoot in the same place twice
        while str(type)[-4:] == "_hit" or str(type)[-5:] == "_miss" or str(type)[-5:] == "_sunk":
            #Resets the x and y coordinates until the location is acceptable
            yAxis = random.randint(0,grid.gridSize-1)
            xAxis = random.randint(0,grid.gridSize-1)
            type = grid.gridReferenceToCoords(userGrid, grid.coordsToGridReference(xAxis, yAxis), None, False)

        if len(foundGame.robotShots) == 0:
            #Make the robot's first shots to always be D4
            xAxis = 3
            yAxis = 3

        #Makes sure to return the (Letter, Number) version of coordinates (Or grid reference)
        coordinates = grid.coordsToGridReference(xAxis, yAxis)

        foundGame.robotShots.append(coordinates)
        
        return coordinates
