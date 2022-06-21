from flask import Flask
from flask import jsonify
from linear_regression import linear_regression
# from TestExample.LinearRegTesting import *

app = Flask(__name__)

model = linear_regression()

@app.route("/")
def hello_world():
    return "Hello World!"
    
@app.route("/predict_class_size")
def predict_class_size():
    # Call function from other py file
    # Store and return the output from the function
    return model.predictSize("test")