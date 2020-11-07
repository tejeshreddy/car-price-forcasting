# Car Price Forcasting
- Deployment of [kaggle challenge](https://www.kaggle.com/nehalbirla/vehicle-dataset-from-cardekho#) on predictive regression on Heroku. This model aims at determing the depreciated price of the car given it's features.


## Steps to Get the App Running on Local
1. Run the below command to setup an python3 environment on local
```bash
bash virtualenv-setup.sh
```

2. To activate the app:
```bash
python app.py
```

## Usage
Once the app is up and running, pass params to `http://127.0.0.1:5000/predict`

#### Parameters

| Parameters | Description | Accepted Values |
| :---: | :---: | :---: |
| year | Year of purchase | 2014, 2015.. |
| present_price | Price(In Lacs) | 6.5 |
| kms_driven | Kms Driven | 2700 |
| fuel_type | Fuel Type | petrol/diesel |
| seller_type | Seller | dealer/individual |
| transmission | Transmission Type | dealer/individual |
| owner | Owner Number | 0, 1, 2 |

#### Example URL

```
http://localhost:5000/predict?year=2014&present_price=5.59&kms_driven=27000&fuel_type=petrol&seller_type=dealer&transmission=mannual&owner=0
```

#### Example Result
```JSON
{
   "params":{
      "year":2014,
      "years_old":6,
      "present_price":5.59,
      "owner":"0",
      "kms_driven":"27000",
      "fuel":{
         "type":"petrol",
         "fuel_type_petrol":1,
         "fuel_type_diesel":0
      },
      "seller_type":{
         "type":"dealer",
         "value":0
      },
      "transmission":{
         "type":"mannual",
         "value":1
      }
   },
   "result":{
      "price":4.58,
      "comment":"Can sell the car for the above price."
   }
}
```

