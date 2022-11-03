import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import requests
import bs4


def multiples(data, name, token_info, current_price, market_cap, returns, days = 30):
    
    '''''''''
    name - unique id in our system
    current_price - most recent token price read from coingecko
    market_cap
    returns - token pct return to be used for calculating volatility
    days - how many days to annualize e.g. 30 would use most recent 30 days of revenue and annualize it
    users - pandas dataframe containing user data
    count - pandas dataframe containing transaction count data 
    '''''''''
    
    volume, fees, revenue, tvl = data[0], data[1], data[2], data[3]
    
    volume = volume[name]
    fees = fees[name]
    revenue = revenue[name]
    
    tvl = tvl.replace('NaN', np.nan)
    tvl = tvl[name]
    
    daily_avg_volume = volume[-days:].mean()
    annualized_volume = daily_avg_volume * 365 
    annualized_fees = fees[-days:].mean() * 365
    annualized_revenue = revenue[-days:].mean() * 365
    

    tvl_current = tvl[np.isnan(tvl)!=True][-1]   
    tvl_turnover = volume[-days:].sum() / tvl[-days:].mean()

    
    price = current_price[name][0]
    std = np.std(returns[name][-days:]) * np.sqrt(365) * 100
    MC = market_cap[-1:][name][0]    
    FDV = price * token_info['Max Supply'][name]
    MC_AF = MC / annualized_fees
    FDV_AF = FDV / annualized_fees
    MC_TVL = MC / tvl_current
    FDV_TVL = FDV / tvl_current
    
    
    
    if annualized_revenue!=0:
        MC_AR = MC / annualized_revenue
        FDV_AR = FDV / annualized_revenue
    
    else:
        MC_AR = np.nan
        FDV_AR = np.nan
    
    circ_max = token_info["% of Circ Supply"][name] 

    
    #if users!=None:
     #   user_table = users[name]
      #  daily_avg_users = user_table[-days:].mean()
       # vol_per_user = (table / user_table)[-days:].mean()
    
    #else:
     #   user_table = np.nan
      #  daily_avg_users = np.nan
       # vol_per_user = np.nan
    
    
    #if count!=None:
     #   transactions = count[name]
      #  daily_avg_transactions = transactions[-days:].mean()

       # vol_per_transaction = (table / transactions)[-days:].mean()
    
    #else:
     #   transactions = np.nan
      #  daily_avg_transactions = np.nan
       # vol_per_transaction = np.nan
        
    #if transactions!=None and users!=None:      
     #   transactions_per_user = (transactions / user_table)[-days:].mean()
    
    #else:
     #   transactions_per_user = np.nan
        
    
    
    titles = ['Daily Average Volume', 'Annualized Volume', 'Annualized Fees (AF)',
         'Annualized Revenue (AR)', 'TVL', 'TVL Turnover ' + str(days) + ' days', 'Token Price', 'Realized Volatility %', 'Market Cap (MC)', 'Fully Diluted Valuation (FDV)',
              'MC / AF', 'FDV / AF', 'MC / AR', 'FDV / AR', 
              'MC / TVL', 'FDV / TVL', '% of Circ Supply']
              #'Daily Average Users', 'Volume per User', 'Daily Average Transactions', 'Volume per Transaction', 'Transactions per User']
    data = [daily_avg_volume, annualized_volume, annualized_fees, 
            annualized_revenue, tvl_current, tvl_turnover, price, std, MC, FDV, 
            MC_AF, FDV_AF, MC_AR, FDV_AR, MC_TVL, FDV_TVL, circ_max]
            #daily_avg_users, vol_per_user, daily_avg_transactions, vol_per_transaction, transactions_per_user]
    
    return pd.DataFrame(data = data, index = titles, columns=[name])



def ratio (numerator, denominator, start, days):
    
    x = numerator[numerator.index == start]
    y = denominator[denominator.index <= start][-days:].mean() * 365
    
    return pd.DataFrame((np.array(x)/np.array(y))[0], index = denominator.columns, columns = [start])

def ratio_TS (numerator, denominator, periods, start = pd.to_datetime(dt.datetime.today().date()) - dt.timedelta(1), days = 30):
    
    
    '''''''''
    Input parameters as following:
    
    - numerator: 
        market cap or fdv
    - denominator: 
        total fees or revenue,
    - periods: 
        how many data points you want to get e.g. market cap / total fees ratio over the past 10 days
    - number of days you want to annualize (e.g. if 30 days, the code will take average of the 30 days of fees and annualize it),
    - start as the starting date (e.g. if today, the code will read marketcap from today and annualize the most recent 30 days of volume, assuming days = 30)
        Coingecko reads new data 8am China time, midnight GMT0, therefore best set start day as today - 1)
    '''''''''
    start = dt.datetime(start.year, start.month, start.day)
    
    starts = pd.date_range(start - dt.timedelta(periods-1), periods = periods)
    
    df = {}
    for i in range(len(starts)):
        df[i] = ratio(numerator, denominator, starts[i], days)
        
    data = pd.concat([df[i] for i in range(len(df))], axis = 1).T
    
    return data     

def multiple_df(df1, df2):
    return df1 * np.array(df2)


def read_maxSupply (url): ### USING COINMARKETCAP
    
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    body = soup.find_all('div', {'class': 'maxSupplyValue'})

    Max_supply = []

    if body == []:
        Max_supply = 'NaN'

    elif body[0].text != '--':    
        Max_supply = body[0].text

    elif body[0].text == '--' and body[1].text != '--':
        Max_supply = body[1].text

    else:
        Max_supply = 'NaN'

    if ',' in Max_supply:
        Max_supply = int(Max_supply.replace(',', ''))
    
    return Max_supply

def token_supply_data(link_, market_cap, price_data, token_id):
    
    '''''''''
    link_ - Conimarketcap links that need to be webscrapped in pd.Series format
    market_cap and price_data to be used to calculate circulating supply, where circulating supply is equal to market cap / price data
    '''''''''

    max_supply = []

    for i in range(len(link_)):
        max_supply.append(read_maxSupply (link_[i]))

    max_supply = pd.DataFrame(data = [max_supply], columns = token_id, index=['Max Supply']).T


    circ_supply = (market_cap / price_data)[-1:]
    circ_supply.index = ['Circulating Supply']
    circ_supply = circ_supply.T

    array = np.array(max_supply)

    if 'NaN' in array: 
        array[array == 'NaN'] = np.nan

    perc = (np.array(circ_supply) / array) * 100 

    perc = pd.DataFrame(perc, columns = ['% of Circ Supply'], index = token_id)

    if (perc>100).sum()[0] !=0:
        perc[list(perc.iloc[:, 0] >= 100)] = 100

    token_info = pd.concat([max_supply, circ_supply, perc], axis=1)
    
    
    return token_info

def order(df):
    
    '''''''''
    Order column a to z. Considering we are operating with multiple dataframes and mixing them, ensuring everything is in order.
    '''''''''
    
    list_ = list(df.columns)
    list_.sort()
    
    df = df[list_]
    
    return df



def get_table(name, data, token_info, current_price, market_cap, returns, days = 30):
    
    '''''''''
    Get multiples for several protocol combined in one table.
    name - unique id in our system
    '''''''''
    
    df = {}
    for i in range(len(name)):
        df[i] = multiples(data = data, name = name[i], token_info = token_info, 
                          current_price = current_price, market_cap = market_cap, returns = returns, days = days)
    
    full_table = (pd.concat([df[i] for i in range(len(df))], axis = 1).T)
    
    return order(full_table.T)

def comp(full_table, protocol1, protocol2):
    
    full_table = full_table.iloc[[0, 2, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15], :]
    
    return pd.DataFrame(np.array(full_table[protocol1] / full_table[protocol2]), columns = [protocol1 + ' / ' + protocol2], index = full_table.index)


def comp_TS(table, protocol1, protocol2):
    
    return table[protocol1] / table[protocol2]


def comp_x_parameters_TS (parameters, descriptive, protocol1, protocol2):
    
    fig, ax = plt.subplots()
    
    for i in range(len(parameters)):
        ax.plot(comp_TS(parameters[i], protocol1, protocol2), label = descriptive[i])
    
    ax.legend()
    plt.title(protocol1 + ' / ' + protocol2)

    return plt.show()


def multiple_versions(versions, descriptive, days):
    
    '''''''''
    Example:
    versions = [uni3_eth dataframe, uni3_opt dataframe]
    descriptive = ['v3 Ethereum', 'v3 Optimism']
    
    Result shows the percentage of activity coming from particular version. Only TVL, volume and fees are covered.
    '''''''''
    
    data = []
    data1 = []
    data2 = []
    for i in range(len(versions)):
        data.append(versions[i]['Volume'][-days:].sum())
        data1.append(versions[i]['TVL'][-1:][0])
        data2.append(versions[i]['Fees'][-days:].sum())

    pct = []
    pct1 = []
    pct2 = []
    for i in range(len(data)):
        pct.append(data[i] / np.array(data).sum() * 100)
        pct1.append(data1[i] / np.array(data1).sum() * 100)
        pct2.append(data2[i] / np.array(data2).sum() * 100)
        
    volume = pd.DataFrame(pct, index=[descriptive], columns=['Volume % Over Last ' + str(days) + ' days'])
    tvl = pd.DataFrame(pct1, index=[descriptive], columns=['TVL %'])
    fees = pd.DataFrame(pct2, index=[descriptive], columns=['Fees % Over Last ' + str(days) + ' days'])
    
    return pd.concat([volume, tvl, fees], axis = 1)


def VFR (volume, fee, revenue_share):
    
    '''''''''
    Get table containing volume, fees and revenue for the particular project. 
    '''''''''
    
    date = volume.index
    volume = np.array(volume.iloc[:, 0])
    fees = volume * fee
    revenue = volume * revenue_share
    
    df = pd.DataFrame([date, volume, fees, revenue], index = ['Date', 'Volume', 'Fees', 'Revenue']).T
    df = df.set_index('Date')
    
    return df