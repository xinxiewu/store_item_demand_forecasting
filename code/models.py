"""
models.py contains tools for Time Series Analysis:
    1. adf_test: Stationary Test by ADF
    2. MyARIMA
"""
import os
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

# adf_test()
def adf_test(df=None, cols=['sales','sales_log', 'sales_diff', 'sales_diff2', 'growth', 'log_growth'], output=r'../public/output', fname='adf_test.csv'):
    """ Generate ADF Test Result

    Args:
        df: input dataframe

    Returns:
        datafram
    """
    i, res = 0, pd.DataFrame(columns=['variable', 't-stat', 'p-val', '1%', '5%', '10%', 'ADF 1%', 'ADF 5%', 'ADF 10%'])
    temp = df.dropna()
    for col in cols:
        test = adfuller(getattr(temp, col))
        res_temp = pd.DataFrame({'variable': col, 't-stat': test[0], 'p-val': test[1],
                                '1%': test[4]['1%'], '5%': test[4]['5%'], '10%': test[4]['10%'], 
                                'ADF 1%': 'Y' if test[0] < test[4]['1%'] else 'N', 
                                'ADF 5%': 'Y' if test[0] < test[4]['5%'] else 'N'
                                ,'ADF 10%': 'Y' if test[0] < test[4]['10%'] else 'N'}, index=[i])
        res = pd.concat([res, res_temp])
        i += 1
    res.to_csv(os.path.join(output,fname), index=False)
    return res

# MyARIMA()
def MyARIMA(df=None, col=None, p=None, d=None, q=None):
    """ Generate ADF Test Result

    Args:
        df: input dataframe

    Returns:
        dataframe
    """
    temp = df.dropna()
    model = ARIMA(getattr(temp, col), order=(p, d, q))
    res = model.fit()
    return pd.DataFrame({'variable': col, 'p': p, 'd': d, 'q': q, 'AIC': res.aic, 'BIC': res.bic}, index=[0])