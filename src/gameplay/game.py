#Importing all the files from the folders
import uuid
from gameplay import grid
from gameplay import units

#Creating the array for every game to be played
games = []

#Creating a class called Game
class Game:
    def __init__ (self, layout):
        #Making the game attributes
        #The id and grids are generated whilst they're being set as an attribute
        self.id = uuid.uuid4()
        self.units = units.layout[layout]
        self.robotGrid = grid.grid(self.units)
        self.userGrid = grid.grid([])
        #Adding this game to the array of games
        games.append(self)

def hitOrMiss(location, id):
    foundGame = None
    #Seaching in the games array for the game with the id that is currently being played
    for index in range(len(games)):
        if str(games[index].id) == str(id):
            foundGame = games[index]
    #Setting the location array of the robots' ships for the game found 
    opponentsSpots = grid.findingShips(foundGame.robotGrid, True, "E")
    for i in range(len(opponentsSpots)):
        #Makes the coordinates A,3 or J,10 into 0,2 or 9,9 respectively
        x = int(ord(opponentsSpots[i][0])) - 65
        y = int(opponentsSpots[i][1:]) - 1
        if location == opponentsSpots[i]:
            type = foundGame.robotGrid[y][x]
            for j in range (len(foundGame.units)):
                #foundGame.units is the units associated to the game being played only
                if type == foundGame.units[j][0]:
                    width = foundGame.units[j][1]
                    length = foundGame.units[j][2]
            #Changes the grid to show the the 'longShip', for example, now says 'longShip_hit'
            foundGame.robotGrid[y][x] = str(foundGame.robotGrid[y][x]) + "_hit"
            coordinatesArray = grid.findingShips(foundGame.robotGrid, False, foundGame.robotGrid[y][x])
            if len(coordinatesArray) == width * length:
                return "sunk", coordinatesArray
            else:
                return True, None
        else:
            i += 1
    return False, None
