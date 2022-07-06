from algorithm import linear_regression
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

model = linear_regression.linear_regression()

@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/predict_class_size", methods=["POST"])
def predict_class_size():
    # Call function from other py file
    # Store and return the output from the function

    # Keep commented until algorithm is fully implemented
    # return model.predict_size("test")

    receivedJSON = request.json
    print(receivedJSON[0])

    # receivedJSON[0]["capacity"] = 299

    return jsonify(receivedJSON)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)