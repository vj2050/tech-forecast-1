import pandas as pd
import fbprophet


class ForecastGenerator:
    def __init__(self, predict_years):
        self.years = predict_years

    def forecast(self, escore_data) -> pd.DataFrame:
        escore_data.rename({"eScore": "y", "cdate": "ds"}, axis='columns', inplace=True)
        prophet = fbprophet.Prophet(changepoint_prior_scale=0.85, seasonality_prior_scale=5)
        prophet.fit(escore_data)
        predict_data = prophet.make_future_dataframe(periods=365 * self.years, freq='D')
        forecast = prophet.predict(predict_data)
        forecast.ds = pd.to_datetime(forecast.ds)
        forecast_simple = pd.DataFrame()
        forecast_simple['val'] = forecast['yhat'].mask(forecast['yhat'].lt(0), 0)
        forecast_simple['date'] = forecast['ds']
        forecast_simple.set_index('date', inplace=True)
        return forecast_simple.resample('MS').sum()
