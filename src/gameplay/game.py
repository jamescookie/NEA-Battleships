import uuid
from gameplay import grid

games = []

#Creating a class called Game
class Game:
    def __init__ (self):
        #Making the game attributes
        #The id and grids are generated whilst they're being set as an attribute
        self.id = uuid.uuid4()
        self.robotGrid = grid.grid()
        self.userGrid = grid.grid()
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
    if location == opponentsSpots[0] or location == opponentsSpots[1] or location == opponentsSpots[2]:
        return True
    else:
        return False
