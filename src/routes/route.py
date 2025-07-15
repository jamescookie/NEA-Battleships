# from flask import request, render_template

def fred(app, render_template):

    #When you type '/' into the browser, this program sends the browser which page to show
    @app.route('/', methods=['GET'])
    def home():
        return render_template('battleships.html')

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
        return render_template('setup.html')
