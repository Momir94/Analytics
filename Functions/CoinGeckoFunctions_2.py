import datetime as dt
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

def get_volume_cg (exchange, days):
    '''''''''
    exchange - exchange name
    days - number of days e.g. 90 will give you volume data for the particular exchange over the most recent 90 days
    '''''''''
    
    data = cg.get_exchanges_volume_chart_by_id (id = exchange, days = days)

    date = []
    volume = []

    for i in range(len(data)):
        date_raw = (dt.datetime.fromtimestamp((data[i][0])/1000))
        date.append(dt.datetime(date_raw.year, date_raw.month, date_raw.day))
        volume.append(float(data[i][1]))
        
    return pd.DataFrame(data = volume, index = date, columns=[exchange])


def dict_to_df (df):
    
    data = df[0].combine_first(df[1])

    for i in range(2, len(df)):
        data = data.combine_first(df[i])
        
    return data

def get_BTC_price (start, end):
    
    btc = get_data_start_to_end('bitcoin', start = start, end = end)
    btc.index = pd.to_datetime(btc.index.date)
    
    return btc


def USD_nominate (table):
    table = table.drop_duplicates()

    btc = get_BTC_price (table.index[0] - dt.timedelta(90), table.index[-1] + dt.timedelta(days=1)) ### - 90 for safety. if data is too recent cg will give me minute data
    
    table = table[table.index <=btc.index[-1]]
    btc = btc.loc[table.index] #cleaning 
    
    table_usd = pd.DataFrame (table.values * btc.values, columns=table.columns, index = table.index)  
    
    return table_usd



def get_data_start_to_end(coin_name, start, end, currency = 'usd', data_type = "prices"):
    '''''''''
    get_data_start_to_end(coin_name = 'bitcoin', start = dt.datetime(2019, 1, 1), dt.datetime(2020, 1, 1))
    data_type could be market_caps or total volumes 
    '''''''''
    data = cg.get_coin_market_chart_range_by_id(id = coin_name, vs_currency = currency, from_timestamp = dt.datetime.timestamp(start), to_timestamp = dt.datetime.timestamp(end))
    data = data[data_type]
    date = []
    price = []
    for i in range(len(data)):
        date.append(dt.datetime.fromtimestamp((data[i][0])/1000))
        price.append(data[i][1])
    
    df = pd.DataFrame(data = price, index = date, columns=[coin_name])
    
    return df

def get_all_versions (exchange):
    
    '''''''''
    Check whether particular exchange has multiple versions as recognized by coingecko
    '''''''''
    
    exchange_list = cg.get_exchanges_id_name_list()
    
    bool_ = []
    for i in range(len(exchange_list)):
        bool_.append(exchange in exchange_list[i]['id'])   
    
    list_ = np.array(exchange_list)[np.array(bool_)]
    
    final = []
    
    for i in range(len(list_)):
        final.append (list_[i]['id'])
    
    return final


def get_market_info(CG_API_id, start = dt.datetime(2020, 1, 1), end = dt.datetime.today()):
    
    '''''''''
    CG_API_id - id of particular token as recognized by coingecko website
    If you choose less than 90 days data you will get hourly data for the particular token. More than 90 days data, you will get daily market information
    '''''''''

    df = {}
    for i in range(len(CG_API_id)):
        df[i] = get_data_start_to_end(CG_API_id[i], start = start, end = end)

    price_data = pd.concat([df[i] for i in range(len(CG_API_id))], axis = 1)
    
    df = {}
    for i in range(len(CG_API_id)):
        df[i] = get_data_start_to_end(CG_API_id[i], start = dt.datetime.today() - dt.timedelta(30), end = dt.datetime.today())
        
    recent_price = pd.concat([df[i] for i in range(len(CG_API_id))], axis = 1)


    df = {}
    for i in range(len(CG_API_id)):
        df[i] = get_data_start_to_end(CG_API_id[i], start = start, end = end, data_type='market_caps')

    market_cap = pd.concat([df[i] for i in range(len(CG_API_id))], axis = 1)

    
    df = {}
    for i in range(len(CG_API_id)):
        df[i] = get_data_start_to_end(CG_API_id[i], start = dt.datetime.today() - dt.timedelta(30), end = dt.datetime.today(), data_type='market_caps')
        
    market_cap_recent = pd.concat([df[i] for i in range(len(CG_API_id))], axis = 1) 
    
    
    price_data.index = pd.to_datetime(price_data.index.date)

    market_cap.index = pd.to_datetime(market_cap.index.date)

    returns = np.log(price_data) - np.log(price_data.shift(1))    
    

    current_price = []
    for i in range(len(recent_price.columns)):
        current_price.append(recent_price[np.isnan(recent_price.iloc[:, i])!=True].iloc[-1, i])

    current_price = pd.DataFrame(data = current_price, index=recent_price.columns, columns=['price']).T
    
    
    current_mc = []
    for i in range(len(market_cap_recent.columns)):
        current_mc.append(market_cap_recent[np.isnan(market_cap_recent.iloc[:, i])!=True].iloc[-1, i])

    current_mc = pd.DataFrame(data = current_mc, index=market_cap_recent.columns, columns=['MC']).T

    
    return market_cap, price_data, returns, current_price, current_mc


def get_usd_volume (exchange, days):
    
    '''''''''
    *** Return daily volume dataframe for the selected exchange.
    
    e.g. exchange  = ['dydx_perpetual']
    
    *** Make sure to have brackets
    
    '''''''''
    
    df = get_volume_cg(exchange, days)
    data = USD_nominate(df)
    
    return data


def get_volume_for_list(list_, days):
    
    '''''''''
    list exchanges as ['exc1', 'exc2']
    '''''''''
    
    df = {}

    for i in range(len(list_)):
        df[i] = get_usd_volume(list_[i], days)

    data = dict_to_df(df)    
    
    return data
