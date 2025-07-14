#importing library called flask, which is a web application (something that recieves requests from a browser and responses from a program)
from flask import Flask, request

#__name__ is a built in python variable of the current program being passed to flask
app = Flask(__name__)

#Creates the path for the browser
#When you type /hello the function runs
@app.route('/hello', methods=['GET'])

def result():
    #The program will say "hello" when you type the URL in
    print("hello")

    #This is what appears on the browser
    return 'Received !'

#If statement is a safety check to make sure flask only runs when the file is run directly and not imported from another file
if __name__ == '__main__':

    #The host='0.0.0.0' is to make every IP address my computer knows about, be able to recieve requests
    app.run(host='0.0.0.0', port=8080)
