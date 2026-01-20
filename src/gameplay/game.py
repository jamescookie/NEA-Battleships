#Importing all the files from the folders
import uuid
from gameplay import grid
from gameplay import units
from flask import jsonify
import importlib

#Creating the array for every game to be played
games = []

#Creating a class called Game
class Game:
    def __init__ (self, layout):
        #Making the game attributes
        #The id and grids are generated whilst they're being set as an attribute
        self.id = uuid.uuid4()
        self.units = units.layout[layout]
        self.robotGrid = grid.grid(self.units, 'robot')
        self.userGrid = None
        #Setting the amount of ships sunken by the user and robot to 0
        self.userShipsSunk = 0
        self.robotShipsSunk = 0
        #Setting the difficulty to nothing so that it can be changed
        self.difficulty = None
        #Adding this game to the array of games
        games.append(self)

#Subroutine to set an attribute
def settingAttr(foundGame, name, value):
    setattr(foundGame, name, value)


def findGame(id):
    foundGame = None
    #Seaching in the games array for the game with the id that is currently being played
    for index in range(len(games)):
        if str(games[index].id) == str(id):
            #Sets 'foundGame' to the uuid of the game being played
            foundGame = games[index]
    return foundGame


def removeGame(id):
    #Finds the uuid of the game in the games array
    for index in range(len(games)):
        if str(games[index].id) == str(id):
            #Removes the uuid from the games array
            games.__delitem__(index)


def hitOrMiss(location, foundGame, board):
    #Making the same code deal with both the user and robot grid and ships they've sunk
    correctGrid = getattr(foundGame, board + "Grid")
    correctShipsSunk = getattr(foundGame, board + "ShipsSunk")
    #Setting the location array of the robots' ships for the game found 
    spots = grid.findingTroops(correctGrid, True, "E")
    for i in range(len(spots)):
        #Makes the coordinates (A,3) or (J,10) into (0,2) or (9,9) respectively
        x = int(ord(spots[i][0])) - 65
        y = int(spots[i][1:]) - 1
        #If the button clicked or random coordinate selected by the robot are 
        #the same coordinates as the location of a ship then:
        if location == spots[i]:
            #Makes 'type' the unit that is in that spot
            type = grid.gridReferenceToCoords(correctGrid, location, None)
            for j in range (len(foundGame.units)):
                #foundGame.units is the units associated to the game being played only
                if type == foundGame.units[j][0]:
                    width = foundGame.units[j][1]
                    length = foundGame.units[j][2]
            #Changes the grid to show the 'longShip', for example, now says 'longShip_hit'
            grid.gridReferenceToCoords(correctGrid, location, (str(type) + "_hit"))
            #Creates a list of every time that instance appears
            coordinatesArray = grid.findingTroops(correctGrid, False, correctGrid[y][x])
            #If statement to check if the every part of the ship has been hit
            if len(coordinatesArray) == width * length:
                #Increments the attribute of the amount of ships sunk by 1 for whoever took the turn
                setattr(foundGame, board + "ShipsSunk", correctShipsSunk + 1)
                return "sunk", coordinatesArray, getattr(foundGame, board + "ShipsSunk")
            else:
                return True, None, None
        else:
            i += 1
    #Allows the robot to not shoot in the same place by marking the empty spot as a missed shot
    grid.gridReferenceToCoords(correctGrid, location, "E_miss")
    return False, None, None


def sinking(hitOrMiss, foundGame, gameId, buttonClicked):
    #If the shot fired has sunk the ship
    if hitOrMiss[0] == 'sunk':
        #If the number fo sunken ships is equal to the number of ships on the board
        if hitOrMiss[2] == len(foundGame.units):
            #Removes the game from the games array because it's not being used anymore
            removeGame(gameId)
            #Tells the JavaScript that the user has won
            return jsonify({"userTurn": {"target": buttonClicked, "result": hitOrMiss[0], 
                                            "coordinates": hitOrMiss[1], "win": True}})
        else:
            #This is the return to JavaScript whether the robot has won, hit or missed
            return robotWinning(hitOrMiss, foundGame, gameId, buttonClicked)
    else:
        #To cover all bases, for example, the user misses, but the robot has sunk and potentially won
        return robotWinning(hitOrMiss, foundGame, gameId, buttonClicked)


def robotWinning(userHitOrMiss, foundGame, gameId, buttonClicked):
    #Importing the correct robot difficulty using dynamic import and only importing the robot needed
    robotType = importlib.import_module("." + str(foundGame.difficulty) + "Robot", 'robots')
    #Fires a random shot at the users board
    robotCoordinates = robotType.robotShooting(foundGame.userGrid)
    #Decides whether the shot sunk, hit or missed a ship
    robotHitOrMiss = hitOrMiss(robotCoordinates, foundGame, "user")
    if robotHitOrMiss[0] == 'sunk':
        if robotHitOrMiss[2] == len(foundGame.units):
            removeGame(gameId)
            #Tells the JavaScript that the user hasn't won, but the robot has
            return jsonify({"userTurn": {"target": buttonClicked, "result": userHitOrMiss[0], 
                                         "coordinates": userHitOrMiss[1], "win": False},
                            "computerTurn": {"target": robotCoordinates, "result": robotHitOrMiss[0], 
                                             "coordinates": robotHitOrMiss[1], "win": True}})
    #Tells the JavaScript that no ships were sunk, and either were hit or missed
    return jsonify({"userTurn": {"target": buttonClicked, "result": userHitOrMiss[0], 
                                 "coordinates": userHitOrMiss[1], "win": False},
                    "computerTurn": {"target": robotCoordinates, "result": robotHitOrMiss[0], 
                                     "coordinates": robotHitOrMiss[1], "win": False}})

#The 'return jsonify' codes are seperated into the users turn and computers turn
#Each one has the target coordinates, whether the shot is successful, 
#all the coordinates of that ship that has already been sunk, whether that is the winning shot
