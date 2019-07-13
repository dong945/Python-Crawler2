# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 11:58:20 2019

@author: dongt
"""

import requests
data = requests.get('https://www.coingecko.com/price_charts/1/twd/90_days.json')
prices = data.json()['stats']

import pandas as pd
df = pd.DataFrame(prices)
df.columns = ['datetime','twd']
df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
df.index = df['datetime']
df['twd'].plot(kind='line', figsize=[10,5])