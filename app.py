from flask import Flask , request , jsonify
import yfinance as yf
import pandas as pd
from prophet import Prophet
app = Flask(__name__)


def make_forecast(ticker, periods, hist='max'):
    stock_data = yf.Ticker(ticker)
    # print("lol")
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

def getStockDataName(ticker):
    stock_data = yf.Ticker(ticker)
  
    # print(hist_data.iloc[-1:]["Open"])
    # print(hist_data.iloc[-2:])
    d = stock_data.get_info()
    print(d)
    return {
     "name" : d["longName"],
     "summary" : d["longBusinessSummary"] if ( "longBusinessSummary" in d) else "",
     "logo" : d["logo_url"],
     "industry" : d["industry"]  if ("industry" in d) else "",

    }
def getStockData(ticker):
    stock_data = yf.Ticker(ticker)
    hist_data = stock_data.history("max", auto_adjust=True)
    # print(hist_data.iloc[-1:]["Open"])
    # print(hist_data.iloc[-2:])
    return {
      "open" : round(hist_data.iloc[-1:]["Open"][0], 2),
      "close" : round(hist_data.iloc[-1:]["Close"][0],2),
      "high" : round(hist_data.iloc[-1:]["High"][0],2),
      "low" : round(hist_data.iloc[-1:]["Low"][0],2),
    }
def getStockTimeData(ticker):
    stock_data = yf.Ticker(ticker)
    hist_data = stock_data.history("max", auto_adjust=True)
    l = []
    for row in hist_data.iloc[-10:].iterrows():
      print("\n")
      print(row[1]["Open"])
      print("\n")
      l.append({
        "open" : round(row[1]["Open"],2),
        "close" : round(row[1]["Close"],2),
        "high" : round(row[1]["High"],2),
        "low" : round(row[1]["Low"],2),
        "date" : row[0]
      })  
    return l

@app.route('/')
def home():
  print(getStockData("ITC.NS"))
  # return jsonify(getStockData("ITC.NS"))
  return "asd"

@app.route('/get-prediction', methods=['POST'])
def predict():
    request_data = request.get_json()
    # send ticker and number of days
    forecast = make_forecast(ticker=request_data["ticker"] , periods=request_data["days"])
    return jsonify({ "details": getStockDataName(request_data["ticker"]), "ticker": request_data["ticker"],  "today": getStockData(request_data["ticker"]),"data10" : getStockTimeData(request_data["ticker"]),  "forecast" : forecast.iloc[-request_data["days"]:, [0,18]].to_dict(orient="records")})  

# listen
if __name__ == "__main__":
#   app.run(port=3000)
  # if you need to make it live debuging add 'debug=True'
  app.run(port=5000, debug=True , host="0.0.0.0")
  