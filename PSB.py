from flask import Flask, render_template, redirect, url_for, request, jsonify
from xgboost import XGBRegressor
import numpy as np
import pandas as pd
import json
import pickle


app = Flask(__name__)
model = pickle.load(open('psb.pkl', 'rb'))

@app.route("/")
def test1():
    return render_template('data.html')

@app.route('/predict', methods=['POST'])
def home():
    data1 = float(request.form['a'])
    data2 = int(request.form['b'])
    data3 = int(request.form['c'])
    data4 = int(request.form['d'])
    data5 = int(request.form['e'])
    data6 = int(request.form['f'])
    data7 = int(request.form['g'])

    df = pd.DataFrame(columns=['ONSPOT_DSTN', 'GOUT_FIRESTTN_NM', 'GOUT_SAFE_CENTER_NM', 'STATMNT_TM',
       'EMRLF_EMD_NM', 'JURISD_DIV_NM_CNT', 'JURISD_DIV_NM_OUT'])
    df = df.append({'ONSPOT_DSTN': data1, 'GOUT_FIRESTTN_NM': data2, 'GOUT_SAFE_CENTER_NM': data3, 'STATMNT_TM': data4,
                    'EMRLF_EMD_NM': data5, 'JURISD_DIV_NM_CNT': data6, 'JURISD_DIV_NM_OUT': data7}, ignore_index=True)
    df2 = df.astype(np.int64)
    df3 = df2.ONSPOT_DSTN.astype(np.float64)
    df2 = df2.drop(columns='ONSPOT_DSTN')
    df4 = pd.concat((df3,df2), axis=1)
    pred = model.predict(df4)
    return render_template('after.html', data=pred)


if __name__ == "__main__":
    app.debug = True
    #app.run(port=80)
    app.run(host="192.168.2.147", port=80)
