
# coding: utf-8

# # 寫一個function

# In[2]:


import requests
import pandas as pd
# Function
def getCoin(url):
    url_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
    data = requests.get(url, headers = url_headers)
    print("status_code:", data.status_code)
    if(data.status_code != 200):        
        return pd.DataFrame({"datetime":"","price":"","value":""})
    # data.state_code=200, 資料為json格式    
    prices = data.json()['stats']
    volumes = data.json()['total_volumes']
    # 轉成dataframe
    df = pd.DataFrame(prices)
    dfV = pd.DataFrame(volumes)
    # 合併
    df['volume'] = dfV[1]  # 成交量
    df.columns = ['datetime','price', 'volume']  # 給column name
    # 將datetime欄位轉成日期格式, 資料取樣為天
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    # 轉成時間序列
    df.index = df['datetime']
    # 回傳DataFrame
    return df

def MovingAverage(df, colPrice, ma):
    colMA = "ma" + str(ma)
    df[colMA] = df[colPrice].rolling(window = ma).mean()
    return df

def BBands(df, colPrice):
    get_ipython().run_line_magic('pylab', 'inline')
    df['ma20'] = df[colPrice].rolling(window = 20).mean()
    df['std20'] = df[colPrice].rolling(window = 20).std()
    df['BB+'] = df['ma20'] + df[colPrice].rolling(window = 20).std()*2
    df['BB-'] = df['ma20'] - df[colPrice].rolling(window = 20).std()*2
    df[[colPrice,'ma20','BB+', 'BB-']].plot(kind = 'line', figsize=[20, 10])
    return df

def Visualize(df, columns):
    get_ipython().run_line_magic('pylab', 'inline')
    df[columns].plot(kind = 'line', figsize=[20, 5])
    
def getFinancilDataSet(url):
    df = getCoin(url)
    df.columns = ['date','close', 'volume']
    Open = [df['close'][0]]
    Open.extend(df['close'][0:-1])
    Close = list(df['close'])
    High = [max(o, c) for o, c in zip(Open, Close)]
    Low = [min(o, c) for o, c in zip(Open, Close)]
    df['open'] = Open
    df['high'] = High
    df['low'] = Low
    cols = ['date','open','high','low','close','volume']
    df = df[cols]
    df.tail(5)
    return df

