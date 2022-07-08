from linear_regression import linear_regression
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

model = linear_regression()


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/predict_class_size", methods=["POST"])
def predict_class_size():
    # Call function from other py file
    # Store and return the output from the function

    receivedJSON = request.json
    indx = 0

    for course in receivedJSON:
        if course["capacity"] != 0:
            # # TODO: course["semester"] will need to be added when the algorithm PR is merged since the func sig changed.
            # currPrediction = model.predict_size(course["subject"] + course["code"])
            # # If this if statement is triggered, it means there was something wrong with connecting to the db.
            # if currPrediction is None:
            #     continue
            currPrediction = course["capacity"]  # TODO: Remove once the algorithm is fully implemented
            receivedJSON[indx]["capacity"] = currPrediction
        indx += 1

    return jsonify(receivedJSON)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
