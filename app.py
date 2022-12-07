from flask import Flask , request , jsonify
import yfinance as yf
import pandas as pd
from prophet import Prophet

app = Flask(__name__)


def make_forecast(ticker, periods, hist='max'):
    stock_data = yf.Ticker(ticker)
    print("lol")
    hist_data = stock_data.history(hist, auto_adjust=True)
    df = pd.DataFrame()
    df['ds'] = hist_data.index.values
    df['ds']= df['ds'].apply(lambda x: x.replace(tzinfo=None))
    df['y'] = hist_data['Close'].values
    m = Prophet(daily_seasonality=False)
    m.fit(df)
    future = m.make_future_dataframe(periods, freq='D')
    forecast = m.predict(future)
    return forecast

@app.route('/')
def home():
  return 'hey!!'

@app.route('/get-prediction', methods=['POST'])
def predict():
    request_data = request.get_json()
    # send ticker and number of days
    forecast = make_forecast(ticker=request_data["ticker"] , periods=request_data["days"])
    return jsonify({ "ticker": request_data["ticker"],  "forecast" : forecast.iloc[-request_data["days"]:, [0,18]].to_dict(orient="records")})
    

# listen
if __name__ == "__main__":
#   app.run(port=3000)
  # if you need to make it live debuging add 'debug=True'
  app.run(port=5000, debug=True)
  