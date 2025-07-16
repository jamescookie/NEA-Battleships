from gameplay import grid
from flask import jsonify

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
        return render_template('single-player.html')

    #Same process but respondes with the multiplayer html instead
    @app.route('/multi-player', methods=['GET'])
    def multiPlayer():
        return render_template('multi-player.html')
    
    #Same process but respondes with the setup html instead
    @app.route('/setup', methods=['POST'])
    def setup():
        #Respondes to the browser with the setup html page and the parameter previousPage, which came from the hidden input from the other pages
        return render_template('setup.html', previousPage = request.form['previous-page'])

    #Same process but respondes with the gameplay html instead
    @app.route('/gameplay', methods=['POST'])
    def gameplay():
        return render_template('battleships.html', gridSize = grid.gridSize)
    
    @app.route('/take-turn', methods=['POST'])
    def takeTurn():
        data = request.get_json()  #Assigning a variable to the information sent from the browser
        if not data:
            return jsonify({"error": "No JSON received"}), 400  #Error handling 
        

        #Button the user has clicked being sent to a subroutine
        #Information to send back to the browser
        return jsonify({"result": grid.hitOrMiss(data.get('turn')), "computer-turn": { "position": "A1", "result": True}})
