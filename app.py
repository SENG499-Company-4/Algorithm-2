from flask import Flask, jsonify, request
import os

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

    # receivedJSON[0]["capacity"] = 299

    return jsonify(receivedJSON)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
