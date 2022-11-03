#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


def get_data (data):
    date = []
    pe = []
    ps = []
    mcap = []
    tvl = []
    gmv = []

    for i in range(len(data)):
        date.append (pd.to_datetime((data[i]['datetime'])))
        pe.append(data[i]['pe'])
        ps.append(data[i]['ps'])
        mcap.append(data[i]['market_cap'])
        tvl.append(data[i]['tvl'])
        gmv.append(data[i]['gmv'])
    
    PE = pd.DataFrame(data = pe, index = date, columns = ['P/E']).iloc[::-1].dropna()
    PS = pd.DataFrame(data = ps, index = date, columns = ['P/S']).iloc[::-1].dropna()
    MC_TVL = pd.DataFrame(data = np.array(pd.Series(mcap) / pd.Series(tvl)), index = date, columns = ['MCAP/TVL']).iloc[::-1].dropna()
    MC_GMV = pd.DataFrame(data = np.array(pd.Series(mcap) / pd.Series(gmv)), index = date, columns = ['MCAP/GMV']).iloc[::-1].dropna()
    
    return PE, PS, MC_TVL, MC_GMV


# In[1]:


# DataFrame with data from TokenTerminal 

def get_volume (data):
    date = []
    volume = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        volume.append(data[i]['gmv'])
    
    VOLUME = pd.DataFrame(data = volume, index = date, columns = ['VOLUME']).iloc[::-1].dropna()
    
    return VOLUME


# In[ ]:

def get_price (data):
    date = []
    price = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        price.append(data[i]['price'])
    
    PRICE = pd.DataFrame(data = price, index = date, columns = ['PRICE']).iloc[::-1].dropna()
    
    return PRICE



# In[ ]:

def get_mcap (data):
    date = []
    mcap = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        mcap.append(data[i]['market_cap'])
    
    MCAP = pd.DataFrame(data = mcap, index = date, columns = ['MCAP']).iloc[::-1].dropna()
    
    return MCAP


# In[ ]:

def get_mcap_circ (data):
    date = []
    market_cap_circulating = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        market_cap_circulating.append(data[i]['market_cap_circulating'])
    
    MARKET_CAP_CIRCULATING = pd.DataFrame(data = market_cap_circulating, index = date, columns = ['market_cap_circulating']).iloc[::-1].dropna()
    
    return MARKET_CAP_CIRCULATING


# In[ ]:

def get_mcap_fully_diluted (data):
    date = []
    market_cap_fully_diluted = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        market_cap_fully_diluted.append(data[i]['market_cap_fully_diluted'])
    
    MARKET_CAP_FULLY_DILUTED = pd.DataFrame(data = market_cap_fully_diluted, index = date, columns = ['market_cap_fully_diluted']).iloc[::-1].dropna()
    
    return MARKET_CAP_FULLY_DILUTED


# In[ ]:

def get_vol_mc (data):
    date = []
    vol_mc = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        vol_mc.append(data[i]['vol_mc'])
    
    VOL_MC = pd.DataFrame(data = vol_mc, index = date, columns = ['vol_mc']).iloc[::-1].dropna()
    
    return VOL_MC


# In[ ]:

def get_pe_circ (data):
    date = []
    pe_circ = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        pe_circ.append(data[i]['pe_circulating'])
    
    PE_CIRC = pd.DataFrame(data = pe_circ, index = date, columns = ['pe_circulating']).iloc[::-1].dropna()
    
    return PE_CIRC


# In[ ]:

def get_pe (data):
    date = []
    pe = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        pe.append(data[i]['pe'])
    
    PE = pd.DataFrame(data = pe, index = date, columns = ['pe']).iloc[::-1].dropna()
    
    return PE


# In[ ]:

def get_ps_circ (data):
    date = []
    ps_circ = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        ps_circ.append(data[i]['ps_circulating'])
    
    PS_CIRC = pd.DataFrame(data = ps_circ, index = date, columns = ['ps_circulating']).iloc[::-1].dropna()
    
    return PS_CIRC


# In[ ]:

def get_ps (data):
    date = []
    ps = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        ps.append(data[i]['ps'])
    
    PS = pd.DataFrame(data = ps, index = date, columns = ['ps']).iloc[::-1].dropna()
    
    return PS


# In[ ]:

def get_tvl (data):
    date = []
    tvl = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        tvl.append(data[i]['tvl'])
    
    TVL = pd.DataFrame(data = tvl, index = date, columns = ['tvl']).iloc[::-1].dropna()
    
    return TVL


# In[ ]:

def get_gmv (data):
    date = []
    gmv = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        gmv.append(data[i]['gmv'])
    
    GMV = pd.DataFrame(data = gmv, index = date, columns = ['gmv']).iloc[::-1].dropna()
    
    return GMV


# In[ ]:

def get_revenue (data):
    date = []
    revenue = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        revenue.append(data[i]['revenue'])
    
    REVENUE = pd.DataFrame(data = revenue, index = date, columns = ['revenue']).iloc[::-1].dropna()
    
    return REVENUE


# In[ ]:

def get_revenue_ss (data):
    date = []
    revenue_ss = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        revenue_ss.append(data[i]['revenue_supply_side'])
    
    REVENUE_SS = pd.DataFrame(data = revenue_ss, index = date, columns = ['revenue_supply_side']).iloc[::-1].dropna()
    
    return REVENUE_SS


# In[ ]:

def get_revenue_p (data):
    date = []
    revenue_p = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        revenue_p.append(data[i]['revenue_protocol'])
    
    REVENUE_P = pd.DataFrame(data = revenue_p, index = date, columns = ['revenue_protocol']).iloc[::-1].dropna()
    
    return REVENUE_P


# In[ ]:

def get_token_incentives (data):
    date = []
    token_incentives = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        token_incentives.append(data[i]['token_incentives'])
    
    TOKEN_INCENTIVES = pd.DataFrame(data = token_incentives, index = date, columns = ['token_incentives']).iloc[::-1].dropna()
    
    return TOKEN_INCENTIVES


# In[ ]:

def get_mc_tvl (data):
    date = []
    mcap = []
    tvl = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        mcap.append(data[i]['mcap'])
        tvl.append(data[i]['tvl'])
    
    MC_TVL = pd.DataFrame(data = np.array(pd.Series(mcap) / pd.Series(tvl)), index = date, columns = ['MCAP/TVL']).iloc[::-1].dropna()
 
    return MC_TVL


# In[ ]:

def get_mc_gmv (data):
    date = []
    mcap = []
    gmv = []

    for i in range(len(data)):
        date.append(pd.to_datetime((data[i]['datetime'])))
        mcap.append(data[i]['mcap'])
        gmv.append(data[i]['gmv'])
    
    MC_GMV = pd.DataFrame(data = np.array(pd.Series(mcap) / pd.Series(gmv)), index = date, columns = ['MCAP/GMV']).iloc[::-1].dropna()
 
    return MC_GMV


def get_all_data (data):
    date = []
    price = []
    mcap = []
    market_cap_circulating = []
    market_cap_fully_diluted = []
    volume = []
    vol_mc = []   
    pe = []
    pe_circulating = []
    ps = []
    ps_circulating = []
    tvl = []
    gmv = []
    revenue = []
    revenue_supply_side = []
    revenue_protocol = []
    token_incentives = []

    for i in range(len(data)):
        date.append (pd.to_datetime((data[i]['datetime'])))
        price.append(data[i]['price']) 
        mcap.append(data[i]['market_cap']) 
        market_cap_circulating.append(data[i]['market_cap_circulating']) 
        market_cap_fully_diluted.append(data[i]['market_cap_fully_diluted']) 
        volume.append(data[i]['volume']) 
        vol_mc.append(data[i]['vol_mc'])   
        pe.append(data[i]['pe']) 
        pe_circulating.append(data[i]['pe_circulating']) 
        ps.append(data[i]['ps']) 
        ps_circulating.append(data[i]['ps_circulating']) 
        tvl.append(data[i]['tvl']) 
        gmv.append(data[i]['gmv'])
        revenue.append(data[i]['revenue']) 
        revenue_supply_side.append(data[i]['revenue_supply_side']) 
        revenue_protocol.append(data[i]['revenue_protocol']) 
        token_incentives.append(data[i]['token_incentives'])
    
    PRICE = pd.DataFrame(data = price, index = date, columns = ['Price']).iloc[::-1].dropna()
    MCAP = pd.DataFrame(data = mcap, index = date, columns = ['MCap']).iloc[::-1].dropna()
    MARKET_CAP_CIRCULATING = pd.DataFrame(data = market_cap_circulating, index = date, columns = ['Market_Cap_Circulating']).iloc[::-1].dropna()
    MARKET_CAP_FULLY_DILUTED = pd.DataFrame(data = market_cap_fully_diluted, index = date, columns = ['Market_Cap_Fully_Diluted']).iloc[::-1].dropna()
    VOLUME = pd.DataFrame(data = volume, index = date, columns = ['Volume']).iloc[::-1].dropna()
    VOL_MC = pd.DataFrame(data = vol_mc, index = date, columns = ['Vol_mc']).iloc[::-1].dropna()
    PE_CIRCULATING = pd.DataFrame(data = pe_circulating, index = date, columns = ['P/E_Circulating']).iloc[::-1].dropna()
    PE = pd.DataFrame(data = pe, index = date, columns = ['P/E']).iloc[::-1].dropna()
    PS_CIRCULATING = pd.DataFrame(data = ps_circulating, index = date, columns = ['P/S_Circulating']).iloc[::-1].dropna()
    PS = pd.DataFrame(data = ps, index = date, columns = ['P/S']).iloc[::-1].dropna()
    TVL = pd.DataFrame(data = tvl, index = date, columns = ['TVL']).iloc[::-1].dropna()
    GMV = pd.DataFrame(data = gmv, index = date, columns = ['GMV']).iloc[::-1].dropna()
    REVENUE = pd.DataFrame(data = revenue, index = date, columns = ['Revenue']).iloc[::-1].dropna()
    REVENUE_SUPPLY_SIDE = pd.DataFrame(data = revenue_supply_side, index = date, columns = ['Revenue_Supply_Side']).iloc[::-1].dropna()
    REVENUE_PROTOCOL = pd.DataFrame(data = revenue_protocol, index = date, columns = ['Revenue_Protocol']).iloc[::-1].dropna()
    TOKEN_INCENTIVES = pd.DataFrame(data = token_incentives, index = date, columns = ['token_incentives']).iloc[::-1].dropna()
    MC_TVL = pd.DataFrame(data = np.array(pd.Series(mcap) / pd.Series(tvl)), index = date, columns = ['MCAP/TVL']).iloc[::-1].dropna()
    MC_GMV = pd.DataFrame(data = np.array(pd.Series(mcap) / pd.Series(gmv)), index = date, columns = ['MCAP/GMV']).iloc[::-1].dropna()
    
    return PRICE, MCAP, MARKET_CAP_CIRCULATING, MARKET_CAP_FULLY_DILUTED, VOLUME, VOL_MC, PE_CIRCULATING, PE, PS_CIRCULATING, PS, TVL, GMV, REVENUE, REVENUE_SUPPLY_SIDE, REVENUE_PROTOCOL, TOKEN_INCENTIVES, MC_TVL, MC_GMV