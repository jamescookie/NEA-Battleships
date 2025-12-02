#Importing all the files from the folders
import uuid
from gameplay import grid
from gameplay import units

#Creating the array for every game to be played
games = []

#Creating a class called Game
class Game:
    def __init__ (self, layout, difficulty):
        #Making the game attributes
        #The id and grids are generated whilst they're being set as an attribute
        self.id = uuid.uuid4()
        self.units = units.layout[layout]
        self.robotGrid = grid.grid(self.units)
        self.userGrid = grid.grid(self.units)
        self.difficulty = difficulty
        #Setting the amount of ships sunken by the user and robot to 0
        self.userShipsSunk = 0
        self.robotShipsSunk = 0
        #Adding this game to the array of games
        games.append(self)


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
    spots = grid.findingShips(correctGrid, True, "E")
    for i in range(len(spots)):
        #Makes the coordinates (A,3) or (J,10) into (0,2) or (9,9) respectively
        x = int(ord(spots[i][0])) - 65
        y = int(spots[i][1:]) - 1
        #If the button clicked or random coordinate selected by the robot are the same coordinates as the location of a ship then:
        if location == spots[i]:
            #Makes 'type' the unit that is in that spot
            type = grid.gridReference(correctGrid, location, None)
            for j in range (len(foundGame.units)):
                #foundGame.units is the units associated to the game being played only
                if type == foundGame.units[j][0]:
                    width = foundGame.units[j][1]
                    length = foundGame.units[j][2]
            #Changes the grid to show the 'longShip', for example, now says 'longShip_hit'
            grid.gridReference(correctGrid, location, (str(type) + "_hit"))
            #Creates a list of every time that instance appears
            coordinatesArray = grid.findingShips(correctGrid, False, correctGrid[y][x])
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
    grid.gridReference(correctGrid, location, "E_miss")
    return False, None, None
