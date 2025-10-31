#Importing files from folders and importing the jsonify file from flask library
from flask import jsonify
from gameplay import game
from gameplay import grid
import importlib

#The creatingRoutes subroutine takes the parameters 'app' and 'render_template' because they're only defined in the main program 
def creatingRoutes(app, request, render_template):

    #When you type '/' into the browser, this program sends the browser which page to show
    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template('index.html')

    #When you click the link, this method runs, which respondes to the browser with the single player html
    #The path and the method on the program and the form have to match up so they can talk to each other
    @app.route('/single-player', methods=['GET'])
    def singlePlayer():
        return render_template('single-player.html', environment = request.args.get('environment'))

    #Same process but respondes with the multiplayer html instead
    @app.route('/multi-player', methods=['GET'])
    def multiPlayer():
        return render_template('multi-player.html')
    
    #Same process but respondes with the setup html instead
    @app.route('/setup', methods=['POST'])
    def setup():
        #Respondes to the browser with the setup html page and the parameter previousPage, which came from the hidden input from the other pages
        return render_template('setup.html', previousPage = request.form['previous-page'], difficulty = request.form['robot'], environment = request.form['environment'])

    #Same process but respondes with the gameplay html instead
    @app.route('/gameplay', methods=['POST'])
    def gameplay():
        #Every time the 'PLAY!!!!' button is clicked a new object in the game class is created (with it's own uuid), it also passes the difficulty of the robot and the map to use
        newGame = game.Game(request.form['environment'], request.form['difficulty'])
        return render_template('battleships.html', gridSize = grid.gridSize, gameId = newGame.id)
    
    #Everytime a button has been clicked by the user, this subroutine will run
    @app.route('/take-turn', methods=['POST'])
    def takeTurn():
        #Assigning a variable to the information sent from the browser
        data = request.get_json() 
        if not data:
            #Error handling (Very unlikely to ever happen)
            return jsonify({"error": "No JSON received"}), 400  
        

        #Button the user has clicked
        buttonClicked = data.get('turn')

        #Gets the Id of the game being played
        gameId =  data.get('id')

        #Sets foundGame to the uuid found in the games array
        foundGame = game.findGame(gameId)

        #Sending the hitOrMiss function what button the user clicked, the uuid of the game being played and that it's the robot's board that's been hit
        hitOrMiss = game.hitOrMiss(buttonClicked, foundGame, "robot")
        #If the shot fired has sunk the ship
        if hitOrMiss[0] == 'sunk':
            #If the number fo sunken ships is equal to the number of ships on the board
            if hitOrMiss[2] == len(foundGame.units):
                #Removes the game from the games array because it's not being used anymore
                game.removeGame(gameId)
                #Tells the JavaScript that the user has won
                return jsonify({"userTurn": {"target": buttonClicked, "result": hitOrMiss[0], "coordinates": hitOrMiss[1], "win": True}})
            else:
                #This is the return to JavaScript whether the robot has won, hit or missed
                return robotWinning(foundGame, gameId, hitOrMiss, buttonClicked)
        else:
            #To cover all bases, for example, the user misses, but the robot has sunk and potentially won
            return robotWinning(foundGame, gameId, hitOrMiss, buttonClicked)

def robotWinning(foundGame, gameId, hitOrMiss, buttonClicked):
    #Importing the correct robot difficulty using dynamic import and only importing the robot needed
    robotType = importlib.import_module("." + str(foundGame.difficulty) + "Robot", 'robots')
    #Fires a random shot at the users board
    robotCoordinates = robotType.robotShooting(foundGame.userGrid)
    #Decides whether the shot sunk, hit or missed a ship
    robotHitOrMiss = game.hitOrMiss(robotCoordinates, foundGame, "user")
    if robotHitOrMiss[0] == 'sunk':
        if robotHitOrMiss[2] == len(foundGame.units):
            game.removeGame(gameId)
            #Tells the JavaScript that the user hasn't won, but the robot has
            return jsonify({"userTurn": {"target": buttonClicked, "result": hitOrMiss[0], "coordinates": hitOrMiss[1], "win": False},
                      "computerTurn": {"target": robotCoordinates, "result": robotHitOrMiss[0], "coordinates": robotHitOrMiss[1], "win": True}})
    #Tells the JavaScript that no ships were sunk, and either were hit or missed
    return jsonify({"userTurn": {"target": buttonClicked, "result": hitOrMiss[0], "coordinates": hitOrMiss[1], "win": False},
                  "computerTurn": {"target": robotCoordinates, "result": robotHitOrMiss[0], "coordinates": robotHitOrMiss[1], "win": False}})

#The 'return jsonify' codes are seperated into the users turn and computers turn
#Each one has the target coordinates, whether the shot is successful, all the coordinates of that ship that has already been sunk, whether that is the winning shot
