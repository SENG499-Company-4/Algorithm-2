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

    receivedJSON = request.json

    # No data was received, therefore return since there is nothing to work on.
    if len(receivedJSON) == 0:
        return jsonify([])

    for course in receivedJSON:
        # TODO: Do we keep ELEC? There are no instances of it in the database.
        if course["subject"] not in ("ECE", "SENG", "CSC", "ELEC"):
            print("Not a core ENGR course, skipping")
            continue

        if not all(key in course for key in ("capacity", "semester", "seng_ratio", "subject", "code")):
            print("Course data is malformed, skipping.")
            continue

        if course["capacity"] != 0:
            currPrediction = model.predict_size(course["subject"] + course["code"], course["semester"])
            # If this if statement is triggered, it means there was something wrong with connecting to the db.
            if currPrediction is None:
                continue

            course["capacity"] = currPrediction[0]

    return jsonify(receivedJSON)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
