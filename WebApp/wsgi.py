#!/usr/bin/env python

import datetime
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from joblib import dump, load

app = Flask(__name__) #Initialize the flask App

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict/<origin>/<dest>/<value_list>', methods=['POST'])
def predict(origin, dest, value_list):
    """
    For performing a prediction!
    """
    (datestr, hour) = value_list.split(',')
    d = datetime.date.fromisoformat(datestr)
    print(d)

    print("Loading pre-trained linear model.")
    model = load("linearmodel.joblib")

    print("Loading all features from pre-trained model.")
    with open('featurenames.pickle', 'rb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        features = pickle.load(f)

    df = pd.DataFrame({"hour": [int(hour)], "weekday": [d.weekday()],
        "month": [d.month], "origin": [origin], "dest": [dest]})
    
    print(df)
    X= pd.get_dummies(data=df) #, drop_first=True)

    for colname in features:
        if colname not in X:
            if colname.startswith("origin_") or colname.startswith("dest_"):
                X[colname] = False
            else:
                print("Unknown Column!", colname)

    X = X.copy()
    X = X[sorted(X.columns)]

    p = model.predict(X)
    print(p[0])
    return jsonify(
        result=p[0])

@app.route('/predict2', methods=['POST'])
def predict2():
    """
    For performing a prediction from static HTML form.
    """
    datestr = request.form['datestr']
    hour = request.form['hour']
    origin = request.form['origin']
    dest = request.form['dest']
    
    d = datetime.date.fromisoformat(datestr)
    print(d)

    print("Loading pre-trained linear model.")
    model = load("linearmodel.joblib")

    print("Loading all features from pre-trained model.")
    with open('featurenames.pickle', 'rb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        features = pickle.load(f)

    df = pd.DataFrame({"hour": [int(hour)], "weekday": [d.weekday()],
        "month": [d.month], "origin": [origin], "dest": [dest]})
    
    print(df)
    X= pd.get_dummies(data=df) #, drop_first=True)

    for colname in features:
        if colname not in X:
            if colname.startswith("origin_") or colname.startswith("dest_"):
                X[colname] = False
            else:
                print("Unknown Column!", colname)

    X = X.copy()
    X = X[sorted(X.columns)]

    p = model.predict(X)
    print(p[0])
    # Return an HTML template, with dictionary of values.
    return render_template('results.html', prediction=round(p[0], 2), origin=origin, dest=dest, hour=hour)

if __name__ == "__main__":
    app.run(debug=True) #is just for development/testing.
    
#    app.run(debug=True, host='0.0.0.0')



