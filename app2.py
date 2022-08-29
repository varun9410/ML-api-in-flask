from flask import Flask,request,jsonify
import pandas as pd
import json
import numpy as np
from datetime import date, timedelta, datetime
from sklearn.ensemble import RandomForestRegressor
from flaml.default import LGBMRegressor
from sklearn.preprocessing import MinMaxScaler
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/prediction',methods=['GET','POST'])
def prediction():
  d=request.data
  jdata = json.loads(d)
  df = pd.DataFrame(jdata, columns=['week','month','year','count'])
  X=df[['week','month','year']].values
  my_date = date.today()
  year,week_num,day_of_week= my_date.isocalendar()
  pred={'week':[week_num+1],'month':[7],'year':year}
  data=pd.DataFrame(pred)
  X_test=data.values
  forecast_df = pd.DataFrame()
  for i in df.columns[3:]:
    y=df[i]
    regressor = RandomForestRegressor(n_estimators =100, random_state =0 )
    estimator = LGBMRegressor()
    estimator.fit(X,y)
    predicted_sale = estimator.predict(X_test)
    forecast=pd.DataFrame()
    forecast['predicted_sale']=predicted_sale
    forecast['dumpdate']=str(date.today())
    forecast['week_no']=(date.today().isocalendar())[1]+1
    forecast['item_id']=i
    forecast_df = pd.concat((forecast_df, forecast[['item_id','week_no','predicted_sale','dumpdate']]),axis=0)
  return forecast_df.to_json(orient="records")

@app.route('/predict_csv',methods=['POST'])
def predict_csv():
  f = request.files['file']
  df=pd.read_csv(f)
  X=df[['week','month','year']].values
  my_date = date.today()
  year,week_num,day_of_week= my_date.isocalendar()
  pred={'week':[week_num+1],'month':[7],'year':year}
  data=pd.DataFrame(pred)
  X_test=data.values
  forecast_df = pd.DataFrame()
  for i in df.columns[3:]:
    y=df[i]
    regressor = RandomForestRegressor(n_estimators =100, random_state =0 )
    estimator = LGBMRegressor()
    estimator.fit(X,y)
    predicted_sale = estimator.predict(X_test)
    forecast=pd.DataFrame()
    forecast['predicted_sale']=predicted_sale
    forecast['dumpdate']=str(date.today())
    forecast['week_no']=(date.today().isocalendar())[1]+1
    forecast['item_id']=i
    forecast_df = pd.concat((forecast_df, forecast[['item_id','week_no','predicted_sale','dumpdate']]),axis=0)
  return forecast_df.to_json(orient="records")

@app.route('/predict_excel',methods=['POST'])
def predict_excel():
  f = request.files['file']
  df=pd.read_excel(f)
  X=df[['week','month','year']].values
  my_date = date.today()
  year,week_num,day_of_week= my_date.isocalendar()
  pred={'week':[week_num+1],'month':[7],'year':year}
  data=pd.DataFrame(pred)
  X_test=data.values
  forecast_df = pd.DataFrame()
  for i in df.columns[3:]:
    y=df[i]
    regressor = RandomForestRegressor(n_estimators =100, random_state =0 )
    estimator = LGBMRegressor()
    estimator.fit(X,y)
    predicted_sale = estimator.predict(X_test)
    forecast=pd.DataFrame()
    forecast['predicted_sale']=predicted_sale
    forecast['dumpdate']=str(date.today())
    forecast['week_no']=(date.today().isocalendar())[1]+1
    forecast['item_id']=i
    forecast_df = pd.concat((forecast_df, forecast[['item_id','week_no','predicted_sale','dumpdate']]),axis=0)
  return forecast_df.to_json(orient="records")

if __name__=='__main__':
  app.run(debug=True)