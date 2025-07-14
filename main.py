#importing library called flask, which is a web application (something that recieves requests from a browser and responses from a program)
from flask import Flask, request, render_template_string

#__name__ is a built in python variable of the current program being passed to flask
app = Flask(__name__)

#Creates the path for the browser
#When you type /hello the function runs
@app.route('/hello', methods=['POST'])

def result():
    #Recieving an input from the web page (should be a first name)
    #.form is the contents from the html code
    name = request.form['firstName']
    print("hello", name)

    #This is what appears on the browser
    return ("hello " + name)

#If statement is a safety check to make sure flask only runs when the file is run directly and not imported from another file
if __name__ == '__main__':

    #The host='0.0.0.0' is to make every IP address my computer knows about, be able to recieve requests
    app.run(host='0.0.0.0', port=8080)
