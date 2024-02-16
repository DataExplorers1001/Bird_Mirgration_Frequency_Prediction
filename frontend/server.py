import json

import pandas as pd
from flask import Flask, request, render_template
import pickle
import  datetime

from datetime import datetime, timedelta
from pmdarima.arima import auto_arima

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset
# import mpld3
# import matplotlib.pyplot as plt
import numpy as np

# load the model
with open('arima_reg.pkl', 'rb') as file:
    model = pickle.load(file)

# create a flask application
app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    # read the file contents and send them to client

    return render_template('index.html')


@app.route("/arima_reg", methods=["POST"])
def arima_reg():
    date = (request.form.get("date"))
    formatted_date = datetime.strptime(date, '%Y-%m-%d')

    dataset_date = datetime(2022, 4, 15)
    days = (formatted_date - dataset_date).days
    print(request.form)
    list_of_pred = []
    # for i in range(int(days)):
    next_day = dataset_date + timedelta(days=1)
    prediction = round((model.predict(start= model.nobs+1, end=model.nobs + days)),3)  # nods = no. of observations
        # list_of_pred.append(prediction)
    series_to_list = prediction.tolist()
    # df = pd.Series(series_to_list)
    # json_in_pred= json.dumps(series_to_list)
    pred = series_to_list

    # return  str(int(pred[-1]))   # prefer the json one
    return  str(int(sum(pred)/len(pred)))
    # return json_in_pred


# @app.route("/predicted", methods=["POST"])
# def predicted():






# start the application
app.run(host="0.0.0.0", port=8000, debug=True)