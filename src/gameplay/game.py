import uuid
from gameplay import grid
from gameplay import units

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
    opponentsSpots = grid.findingShips(foundGame.robotGrid)
    i = 0
    for i in range(len(opponentsSpots)):
        if location == opponentsSpots[i]:
            return True
        else:
            i += 1
    return False
