# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 13:11:06 2021

@author: Kojofl
"""

import pandas as pd 
import numpy as np
import datetime 

data = pd.read_csv('leerverkaeufe.csv')

today = datetime.date.today()
for isin in set(data['ISIN']):
    partial_data = data[data['ISIN'] == isin]
    for pos in set(partial_data['Positionsinhaber']):
        
        positionsinhaber_partial = partial_data[partial_data['Positionsinhaber'] == pos]
        
        save = positionsinhaber_partial
        
        idx = pd.date_range(positionsinhaber_partial.iloc[-1]['Datum'], today.strftime("%Y-%m-%d"))
        
        idx_date = idx.date
        
        positionsinhaber_daten = positionsinhaber_partial.reindex(idx_date)
        
        positionsinhaber_daten['Positionsinhaber'] = pos
        
        positionsinhaber_daten['ISIN'] = isin
        
        positionsinhaber_daten['Emittent'] = partial_data.iloc[0]['Emittent']
        
        positionsinhaber_daten = positionsinhaber_daten.drop(['Datum'], axis=1)
        
        for index, el in save.iterrows():
            
            date_time_obj = datetime.datetime.strptime(el['Datum'], '%Y-%m-%d')
            
            date_time = date_time_obj.date()
            
            if date_time in positionsinhaber_daten.index:
                
                positionsinhaber_daten.loc[date_time]['Position'] = el['Position']   
        
        positionsinhaber_daten = positionsinhaber_daten.sort_index(ascending=False)
        
        positionsinhaber_daten = positionsinhaber_daten.bfill()
    
    f = open("dataset.txt", "a")
    
    with f as outfile:
        positionsinhaber_daten.to_string(outfile)
        