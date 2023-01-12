import numpy as np
import pyramid
import pandas
import csv  

print('numpy version: %r' % np.__version__)
print('pyramid version: %r' % pyramid.__version__)


wineind = pandas.read_csv('d1cffab03796e70716c880f1f9d8cb64unpickle_train.csv')
wineind = wineind.iloc[:,0].values
from pyramid.arima import ARIMA

fit = ARIMA(order=(1, 1, 1), seasonal_order=(0, 1, 1, 12)).fit(y=wineind)

fit = ARIMA(order=(1, 1, 1), seasonal_order=None).fit(y=wineind)

from pyramid.arima import auto_arima

stepwise_fit = auto_arima(wineind, start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                          start_P=0, seasonal=True, d=1, D=1, trace=True,
                          error_action='ignore',  # don't want to know if an order does not work
                          suppress_warnings=True,  # don't want convergence warnings
                          stepwise=True)  # set to stepwise
f = (open('result.csv','wb'))
f.write(stepwise_fit.summary().as_csv())

rs_fit = auto_arima(wineind, start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                    start_P=0, seasonal=True, n_jobs=-1, d=1, D=1, trace=True,
                    error_action='ignore',  # don't want to know if an order does not work
                    suppress_warnings=True,  # don't want convergence warnings
                    stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
                    n_fits=25)

print rs_fit.summary().as_csv()


from bokeh.plotting import figure, show, output_notebook
import pandas as pd

# init bokeh
output_notebook()

def plot_arima(truth, forecasts, title="ARIMA", xaxis_label='Time',
               yaxis_label='Value', c1='#A6CEE3', c2='#B2DF8A', 
               forecast_start=None, **kwargs):
    
    # make truth and forecasts into pandas series
    n_truth = truth.shape[0]
    n_forecasts = forecasts.shape[0]
    
    # always plot truth the same
    truth = pd.Series(truth, index=np.arange(truth.shape[0]))
    
    # if no defined forecast start, start at the end
    if forecast_start is None:
        idx = np.arange(n_truth, n_truth + n_forecasts)
    else:
        idx = np.arange(forecast_start, n_forecasts)
    forecasts = pd.Series(forecasts, index=idx)
    
    # set up the plot
    p = figure(title=title, plot_height=400, **kwargs)
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = xaxis_label
    p.yaxis.axis_label = yaxis_label
    
    # add the lines
    p.line(truth.index, truth.values, color=c1, legend='Observed')
    p.line(forecasts.index, forecasts.values, color=c2, legend='Forecasted')
    
    return p



in_sample_preds = stepwise_fit.predict_in_sample()
in_sample_preds[:10]


show(plot_arima(wineind, in_sample_preds, 
                title="Original Series & In-sample Predictions", 
                c2='#FF0000', forecast_start=0))


next_25 = stepwise_fit.predict(n_periods=25)

show(plot_arima(wineind, next_25))


updated_data = np.concatenate([wineind, next_25])
updated_model = stepwise_fit.fit(updated_data)
updated_model.summary()


show(plot_arima(updated_data, updated_model.predict(n_periods=10)))

