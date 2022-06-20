from flask import Flask, jsonify, request

# from TestExample.LinearRegTesting import *

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/predict_class_size", methods=["POST"])
def predict_class_size():
    # Call function from other py file
    # Store and return the output from the function

    receivedJSON = request.json
    print(receivedJSON[0])
    receivedJSON[0]["capacity"] = 299

    return jsonify(receivedJSON)
    # return "Class Capacity: 45" + "\n\n" + "We did it!"
