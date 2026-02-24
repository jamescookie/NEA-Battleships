#Importing files from folders and importing the jsonify file from flask library
from flask import jsonify
from gameplay import game
from gameplay import grid

#The creatingRoutes subroutine takes the parameters 'app' and 'render_template' 
#because they're only defined in the main program 
def creatingRoutes(app, request, render_template):

    #When you type '/' into the browser, this program sends the browser which page to show
    @app.route('/', methods=['GET', 'POST'])
    def home():

        #This checks to see if this page was reached from going back a page or not
        #In this case the 'not' would be from typing the correct URL into the browser
        if request.method == "POST":
            #Whenever going back to the home page, any game that was created, would be removed
            game.removeGame(request.form['gameId'])

        return render_template('index.html')

    #When you click the link, this method runs, which responds to the browser with the single player html
    #The path and the method on the program and the form have to match up so they can talk to each other
    @app.route('/single-player', methods=['GET', 'POST'])
    def singlePlayer():

        #Same as before, but will instead create a new game when travelling forward through the pages
        if request.method == "GET":
            newGame = game.Game(request.args.get('environment'))
        #And collecting information from the already created game if not
        else:
            newGame = game.findGame(request.form['gameId'])


        #Responds to the browser with the single-player html page and the parameters:
        # gameId, which has just been created
        # units, which come from the game (these need to be convented into json)
        # gridSize, which comes from the grid

        return render_template('single-player.html', gameId = newGame.id, 
                               units = newGame.units, gridSize = grid.gridSize)

    #Same process but responds with the multiplayer html instead
    @app.route('/multi-player', methods=['GET'])
    def multiPlayer():
        return render_template('multi-player.html')
    
    #Same process but responds with the setup html instead
    @app.route('/setup', methods=['POST'])
    def setup():
        
        #Gets the Id of the game being played
        gameId = request.form['gameId']

        #Sets foundGame to the uuid found in the games array
        foundGame = game.findGame(gameId)

        #Uses the settingAttr subroutine to change the difficulty of the robot you will be playing,
        #from None to whatever button you clicked on
        game.settingAttr(foundGame, 'difficulty', request.form['robot'])

        # previousPage, which came from the hidden input from the other pages
        #This sends the same parameters as before, but also previousPage for single player or multiplayer,
        #depending on where the user came from
        return render_template('setup.html', previousPage = request.form['previous-page'], 
                               gameId = foundGame.id, units = foundGame.units, 
                               gridSize = grid.gridSize)

    #This subroutine is to check whether all the units are within the grid
    @app.route('/validate-board', methods=['POST'])
    def validateBoard():
        data = request.get_json()
        gameId = data.get('gameId')
        board = data.get('board')
        #Sets foundGame to the uuid found in the games array
        foundGame = game.findGame(gameId)
        
        numOfUnits = grid.numberOfUnits(foundGame.units)
        numberOfUnitsOnBoard = grid.findingTroops(board, False, "E")
        #If how many empty spaces + how many troops in the game add to make the entire grid
        if len(numberOfUnitsOnBoard) + numOfUnits[0] == numOfUnits[1] * numOfUnits[1]:
            #Sets the userGrid in the game to be the board the user made, only if it's valid
            game.settingAttr(foundGame, 'userGrid', board)
            grid.printingGrid(board, 'user')
            return jsonify({"valid" : True, "message" : "board is vaid"})
        else:
            return jsonify({"valid" : False, "message" : "Some units are off the board"})
        

    #Same process but responds with the gameplay html instead
    @app.route('/gameplay', methods=['POST'])
    def gameplay():

        #Gets the Id of the game being played
        gameId = request.form['game-id']

        #Sets foundGame to the uuid found in the games array
        foundGame = game.findGame(gameId)

        #Checks to see if the random button was clicked
        if request.form['random'] == "random":

            #Uses the settingAttr subroutine to change the userGrid to random
            game.settingAttr(foundGame, 'userGrid', grid.grid(foundGame.units, 'user'))

            return render_template('battlematrix.html', gridSize = grid.gridSize, gameId = gameId)

        else:
            #Every time the 'PLAY!!!!' button is clicked a new object in the game class is created
            #(with it's own uuid), it also passes the difficulty of the robot and the map to use
            return render_template('battlematrix.html', gridSize = grid.gridSize, gameId = gameId)
    
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

        #Sending the hitOrMiss function what button the user clicked, the uuid of the game being played and 
        #that it's the robot's board that's been hit
        hitOrMiss = game.hitOrMiss(buttonClicked, foundGame, "robot")

        #This is the subroutine for when the users shot has been registered
        #and to determine whether they have won or not, or whether the robot needs to shoot as well
        #Needs to return the value, otherwise the 'turn' won't end
        return game.sinking(hitOrMiss, foundGame, gameId, buttonClicked)
