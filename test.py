import yfinance as yf
import pandas as pd
from prophet import Prophet
def make_forecast(ticker, periods, hist='max'):
    """
    forecast the given ticker (stock) period days into the future (from today)

    inputs
    ------
    > ticker
        >> ticker of stock to forecast
    > periods
        >> number of days into the future to forecast (from today's date)
    > hist
        >> amount of historical data to consider
            > default: max
            > options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    """
    # pull historical data from yahoo finance
    stock_data = yf.Ticker(ticker)
    print("lol")
    hist_data = stock_data.history(hist, auto_adjust=True)
    # create new dataframe to hold dates (ds) & adjusted closing prices (y)
    df = pd.DataFrame()
    df['ds'] = hist_data.index.values
    df['ds']= df['ds'].apply(lambda x: x.replace(tzinfo=None))
    df['y'] = hist_data['Close'].values
    # create a Prophet model from that data
    m = Prophet(daily_seasonality=False)
    m.fit(df)
    future = m.make_future_dataframe(periods, freq='D')
    forecast = m.predict(future)
    m.plot(forecast)
    return forecast

res = make_forecast('KREF', 180)
# print(res.iloc[-2:]["ds"])
print(res.iloc[-3:, [0,18]].to_dict(orient="records"))
print(res.tail())
