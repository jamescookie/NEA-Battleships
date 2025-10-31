#importing library called flask, which is a web application (something that recieves requests from a browser and responses from a program)
from flask import Flask, request, render_template

#__name__ is a built in python variable of the current program being passed to flask
app = Flask(__name__)

#From the folder 'routes', the code is importing the file 'route'
from routes import route

#In the file 'route', the subroutine 'creatingRoutes' is taking the arguements
route.creatingRoutes(app, request, render_template)

#If statement is a safety check to make sure flask only runs when the file is run directly and not imported from another file
if __name__ == '__main__':

    #The host='0.0.0.0' is to make every IP address my computer knows about, be able to recieve requests
    app.run(host='0.0.0.0', port=8080, debug=True)
