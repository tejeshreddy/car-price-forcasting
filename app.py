import json
import pickle
import sklearn
import jsonify
import requests
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from flask import Flask, render_template, request, Response

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

standard_to = StandardScaler()

@app.route('')
def index():
    return "Welcome to the app!"

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    year = int(request.args.get("year"))
    present_price = float(request.args.get('present_price'))
    kms_driven = np.log(int(request.args.get('kms_driven')))
    fuel_type = request.args.get("fuel_type")
    owner = request.args.get("owner")
    
    if fuel_type == "petrol":
        fuel_type_petrol = 1
        fuel_type_diesel = 0
    elif fuel_type == "diesel":
        fuel_type_petrol = 0
        fuel_type_diesel = 1
    else:
        fuel_type_petrol = 0
        fuel_type_diesel = 0
    
    years_old = datetime.now().year - year
    
    seller_type = request.args.get("seller_type")
    if seller_type == "individual":
        seller_type = 1
    else:
        seller_type = 0
    
    transmission = request.args.get("transmission")
    if transmission == "mannual":
        transmission = 1
    else:
        transmission = 0
    
    prediction=model.predict([[present_price, kms_driven, owner, years_old, fuel_type_diesel, 
                               fuel_type_petrol, seller_type, transmission]])
    output=round(prediction[0],2)
    
    json_res = {
        "params": {
            "year": year,
            "years_old": years_old,
            "present_price": present_price,
            "owner": owner,
            "kms_driven": request.args.get('kms_driven'),
            "fuel": {
                "type": fuel_type,
                "fuel_type_petrol": fuel_type_petrol,
                "fuel_type_diesel": fuel_type_diesel
            },
            "seller_type": {
                "type": request.args.get("seller_type"),
                "value": seller_type
            },
            "transmission": {
                "type": request.args.get("transmission"),
                "value": transmission
            }
        },
        "result": {
            "price": output,
            "comment": "Can sell the car for the above price." if output > 0 else "Can't sell car"
        }
    }
    
    resp = Response(json.dumps(json_res), status=200, mimetype='application/json')
    return resp
    

if __name__=="__main__":
    app.run(debug=True)
