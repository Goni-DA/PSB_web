from flask import Flask, render_template, redirect, url_for, request, jsonify
from xgboost import XGBRegressor
import numpy as np
import pandas as pd
import json
import pickle
import PSB_manage as pm

app = Flask(__name__)
model = pickle.load(open('data2.pkl', 'rb')) # 모델 Input (XGBoost)

@app.route('/predict', methods=['POST'])
# @app.route('/', methods=['GET'])

def home():

    # GEt 방식 변수받기
    # data1 = request.args.get('fire', type = int) # 삭제예정
    # data10 = request.args.get('emr', type = str) # 신고동이름 ex. 고덕동
    # data5 = request.args.get('rel', type = int) # 사건발생장소 ex. 1
    # data6 = request.args.get('stat', type = int) # 신고시각 ex. 12
    # data7 = request.args.get('jur', type = int) # 관할구역 ex. 1
    # data8 = request.args.get('x', type = float) # 위도 ex.38.6417
    # data9 = request.args.get('y', type = float) # 경도 ex.125.788109

    # 제이슨 데이터 받기
    jsonData = request.get_json()

    # # 제이슨 객체 내 요소들 변수에 받기
    # data1 = int(jsonData['fire'])
    data1 = 1
    data10 = str(jsonData['emr'])
    data5 = int(jsonData['rel'])
    data6 = int(jsonData['stat'])
    data7 = int(jsonData['jur'])
    data8 = float(jsonData['x'])
    data9 = float(jsonData['y'])

    print(data10)
    print(data5)
    print(data6)
    print(data7)
    print(data8)
    print(data9)


    if ((data8 == None) | (data9 == None)|(data10 == None)):
        return "좌표변수는 필수입니다."
    else:
        # dist_only : 현장과의 거리 계산
        data3 = pm.dist_only(data8, data9)
        # get_safe : 안전센터 레이블 반환
        data2 = pm.get_safe(data8, data9)
        # 동이름 반환
        data4 = pm.get_donginfo(data10)

    #안전센터 좌표
    add_safe = pm.get_safe_geo(data2)

    print("safe 좌표")
    print(add_safe)

    # 예측(모델 학습을 np.array로 시켜서 예측도 np.array로 진행함)
    arr = np.array([[data1, data2, data3, data4, data5, data6, data7]])
    pred = model.predict(arr)

    # 배열/튜플로 넘어오는 예측값을 json객체로 반환함
    answer = str(round(float(pred[0])))
    safe_long = str(float(add_safe[0]))
    safe_lat = str(float(add_safe[1]))

    print(answer)
    if ((data1 == None) | (data4 == None)| (data5 == None)|
            (data6 == None)| (data7 == None)):
        return "귀하가 보내주신 변수이름에 오류가 있습니다. 수정하세요."
    else :
        return jsonify({"answer": answer,
                        "safe_long" : safe_long,
                        "safe_lat" : safe_lat,
                        "pick_long" : data9,
                        "pick_lat" : data8})

if __name__ == "__main__":
    app.debug = True
    #app.run(port=80)
    app.run(host="192.168.2.147", port=80)
