import requests
import pandas as pd
import numpy as np
import datetime as dt
import FundamentalFunctions as ff
from itertools import compress




def protocol_slug(protocol):

    url = 'https://api.llama.fi/protocols'
    r = requests.get(url)
    data = r.json()
    
    llama_ids = []
    for i in range(len(data)):
        llama_ids.append(data[i]['slug'])

    bool_ = []
    for i in range(len(llama_ids)):
        bool_.append(protocol in llama_ids[i]) 

    return np.array(llama_ids)[np.array(bool_)][0]
    

def get_tvl(protocol_slug):
    
    url = 'https://api.llama.fi/protocol/' + protocol_slug
    r = requests.get(url)
    data = r.json()

    date = []
    tvl = []

    for i in range(len(data['tvl'])):
        date_ = dt.datetime.fromtimestamp(data['tvl'][i]['date'])
        date_ = date_ - dt.timedelta(hours = 8) ## To standardize time zone
        date.append(dt.datetime(date_.year, date_.month, date_.day))
        tvl.append(data['tvl'][i]['totalLiquidityUSD'])

    tvl = pd.DataFrame([date, tvl], index = ['Date', protocol_slug + 'TVL']).T
    tvl = tvl.set_index('Date')
    tvl = tvl.sort_index()
    
    return tvl
    
def get_tvl_for_chain(protocol_slug, chain):
    
    url = 'https://api.llama.fi/protocol/' + protocol_slug
    r = requests.get(url)
    data = r.json()

    date = []
    tvl = []

    for i in range(len(data['chainTvls'][chain]['tvl'])):
        date_ = dt.datetime.fromtimestamp(data['chainTvls'][chain]['tvl'][i]['date'])
        date_ = date_ - dt.timedelta(hours = 8) ## To standardize time zone
        date.append(dt.datetime(date_.year, date_.month, date_.day))
        tvl.append(data['chainTvls'][chain]['tvl'][i]['totalLiquidityUSD'])

    tvl = pd.DataFrame([date, tvl], index = ['Date', protocol_slug + 'TVL']).T
    tvl = tvl.set_index('Date')
    tvl = tvl.sort_index()
    
    return tvl


def num_of_supported_chains(slug):
    
    '''''''''
    slug - list of protocols' defillama ids e.g. ['mcdex'] or ['mcdex', 'dydx']
    '''''''''
    
    url = 'https://api.llama.fi/protocols'
    r = requests.get(url)
    data = r.json()

    llama_ids = []
    for i in range(len(data)):
        llama_ids.append(data[i]['slug'])

    chains = []
    for i in range(len(data)):
        chains.append(data[i]['chains'])

    df = pd.DataFrame(data=[llama_ids, chains], index = ['Protocol Slug', 'Chains']).T
    df = df.set_index('Protocol Slug')    
    
    num_chains = []
    for i in range(len(slug)):
        int_ = np.where(df.index == slug[i])[0][0]
        num_chains.append(len((df.iloc[int_].values)[0]))
    
    return pd.DataFrame(num_chains, index = slug, columns = ['# of chains DL'])



def get_tvl_full(protocols, dl_slug, names, num_chains):
    
    '''''''''
    Get TVL for list of protocols.
    
    If our data matches that of the defillama then read TVL directly. If not, then first check what chains to we cover, and then specifically call data for those chains on defillama.
    
    protocols - dictionary containing all information for protocols in question
    dl_slug - list of slugs according to defillama
    names - protocols as recognized internally 
    num_chains - dataframe containing protocols and number of chains included in our analysis
    '''''''''

    num_chains_dl = num_of_supported_chains(dl_slug)
    num_chains_dl.index = names
    
    bool_ = ((num_chains['# of chains']) == (num_chains_dl['# of chains DL']))

    matching = list(compress(names, bool_)) #where our data matches defillama data
    unmatched = list(compress(names, (bool_ == False)))

    tvl = {}

    for i in range(len(matching)):
        tvl[i] = (get_tvl(matching[i]))

    tvl = pd.concat([tvl[i] for i in range(len(tvl))], axis = 1)
    tvl.columns = matching

    tvl1 = {}

    for i in range(len(unmatched)):    
        tvl1[i] = {}
        for z in range(len(protocols[unmatched[i]]['ecosystem'])):
            tvl1[i][z] = (get_tvl_for_chain(unmatched[i], protocols[unmatched[i]]['ecosystem'][z]))

        tvl1[i] = pd.concat([tvl1[i][z] for z in range(len(protocols[unmatched[i]]['ecosystem']))], axis = 1)
        tvl1[i] = tvl1[i].sum(axis = 1)

        tvl1[i] = pd.DataFrame(tvl1[i].values, index = tvl1[i].index, columns=[unmatched[i]])

    tvl1 = pd.concat([tvl1[i] for i in range(len(tvl1))], axis = 1)

    tvl_full = pd.concat([tvl, tvl1], axis = 1)
    tvl_full = ff.order(tvl_full)
    
    return tvl_full


def supported_chains(slug):
    
    '''''''''
    slug - list of protocols' defillama ids e.g. ['mcdex'] or ['mcdex', 'dydx']
    '''''''''
    
    url = 'https://api.llama.fi/protocols'
    r = requests.get(url)
    data = r.json()

    llama_ids = []
    for i in range(len(data)):
        llama_ids.append(data[i]['slug'])

    chains = []
    for i in range(len(data)):
        chains.append(data[i]['chains'])

    df = pd.DataFrame(data=[llama_ids, chains], index = ['Protocol Slug', 'Chains']).T
    df = df.set_index('Protocol Slug') 
    
    chains = []
    for i in range(len(slug)):
        int_ = np.where(df.index == slug[i])[0][0]
        chains.append(df.iloc[int_].values)
    
    return pd.DataFrame(chains, index = slug, columns = ['Chains'])


def get_tvl_multichain(chains, protocol_slug):
    
    '''''''''
    chains e.g. ['Binance', 'Heco']
    '''''''''
    
    url = 'https://api.llama.fi/protocol/' + protocol_slug
    r = requests.get(url)
    data = r.json()
    
    df = {}
    for i in range(len(chains)):
        df[i] = data['chainTvls'][chains[i]]
    
    
    tvl_ = {}
    for z in range(len(df)):
        
        date = []
        tvl = []

        for i in range(len(df[z]['tvl'])):
            date_ = dt.datetime.fromtimestamp(df[z]['tvl'][i]['date'])
            date_ = date_ - dt.timedelta(hours = 8) ## To standardize time zone
            date.append(dt.datetime(date_.year, date_.month, date_.day))
            tvl.append(df[z]['tvl'][i]['totalLiquidityUSD'])

        tvl = pd.DataFrame([date, tvl], index = ['Date', chains[z] + 'TVL']).T
        tvl = tvl.set_index('Date')
        tvl = tvl.sort_index()
        
        tvl_[z] = tvl
    
    return tvl_