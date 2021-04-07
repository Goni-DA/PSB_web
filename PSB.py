from flask import Flask, render_template, redirect, url_for, request, jsonify
from xgboost import XGBRegressor
import numpy as np
import pandas as pd
import sklearn
import json
import pickle
import PSB_manage as pm


app = Flask(__name__)
model = pickle.load(open('data.pkl', 'rb'))
cols_check = model.get_booster().feature_names

@app.route("/")
def test1():
    return render_template('data.html')

@app.route('/predict', methods=['POST'])
def home():
    data1 = int(request.form['a'])
    #data2 = int(request.form['b']) #safe_center
    #data3 = float(request.form['c']) #onspot
    data4 = int(request.form['d'])
    data5 = int(request.form['e'])
    data6 = int(request.form['f'])
    data7 = int(request.form['g'])
    data8 = float(request.form['h'])
    data9 = float(request.form['i'])

    data2 = pm.dist(data8, data9)
    data3 = pm.dist_only(data8, data9)


    df = pd.DataFrame(columns=['GOUT_FIRESTTN_NM', 'GOUT_SAFE_CENTER_NM', 'ONSPOT_DSTN',
       'EMRLF_EMD_NM', 'RELIF_OCCURPLC_TYPE', 'STATMNT_TM','JURISD_DIV_NM_CNT'])
    df = df.append({'GOUT_FIRESTTN_NM': data1, 'GOUT_SAFE_CENTER_NM': data2, 'ONSPOT_DSTN': data3, 'EMRLF_EMD_NM': data4,
                    'RELIF_OCCURPLC_TYPE': data5, 'STATMNT_TM': data6, 'JURISD_DIV_NM_CNT': data7}, ignore_index=True)
    df2 = df.astype(np.int64)
    df3 = df2.ONSPOT_DSTN.astype(np.float64)
    df2 = df2.drop(columns='ONSPOT_DSTN')
    df4 = pd.concat((df3,df2), axis=1)
    df4 = df4[cols_check]

    pred = model.predict(df4)
    return render_template('after.html', data=pred)


if __name__ == "__main__":
    app.debug = True
    #app.run(port=80)
    app.run(host="192.168.2.147", port=80)
