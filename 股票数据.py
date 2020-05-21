import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader
from pandas.util.testing import assert_frame_equal
import pandas_datareader.data as web

# aapl=pandas_datareader.DataReader('AAPL', 'yahoo')
# goog=pandas_datareader.DataReader('GOOG', 'yahoo')
# baba=pandas_datareader.DataReader('BABA', 'yahoo')
# amzn=pandas_datareader.DataReader('AMZN', 'yahoo')

print(dir(web))
goog = web.DataReader('GOOG', 'yahoo')
print(goog)
