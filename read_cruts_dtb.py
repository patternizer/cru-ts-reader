#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# CRU TS v4.04 .dtb reader
#------------------------------------------------------------------------------
# Version 0.1
# 5 August, 2021
# Michael Taylor
# https://patternizer.github.io
# patternizer AT gmail DOT com
# michael DOT a DOT taylor AT uea DOT ac DOT uk
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# IMPORT PYTHON LIBRARIES
#------------------------------------------------------------------------------
import numpy as np
import pandas as pd

# Silence library version notifications
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# SETTINGS: 
#------------------------------------------------------------------------------

filename_txt = 'DATA/tmp.2103041709.clean.dtb'
    
#------------------------------------------------------------------------------
# METHODS
#------------------------------------------------------------------------------

def load_dataframe(filename_txt):
    
    # load .dtb file into pandas dataframe

    # station header sample:    
    # 0000300 -1650  -6820 4060 LA.PAZ.EL.ALTO       BOLIVIA       1918 1990
    # station data sample:
    # 6190-9999-9999-9999-9999-9999-9999-9999-9999-9999-9999-9999-9999
    # 1918   84   84   94   95   85   74   63   84   93   98  112  108
        
    yearlist = []
    monthlist = []
    stationcode = []
    stationlat = []
    stationlon = []
    stationelevation = []
    stationname = []
    stationcountry = []
    stationfirstyear = []
    stationlastyear = []
    
    with open(filename_txt, 'r', encoding="ISO-8859-1") as f:  
                    
        for line in f:   

            if len(line.strip().split())>1: # extract station header and data

                if len(line.strip().split()[0]) > 4:                
                    if line.strip().split()[0][4].isdigit():

                        print(line)
                        words = line.strip().split()
                        code = words[0]
                        lat = words[1]
                        lon = words[2]
                        elevation = words[3]
                        name = words[4:-3]    
                        country = words[-3]
                        firstyear = words[-2]
                        lastyear = words[-1]                                                
                else:           
                    yearlist.append(line[0:4])                                
                    obs = []
                    for i in range(12):
                        obs.append(line[4+5*i:4+5*(i+1)])    
                    monthlist.append(np.array(obs))                                 
                    stationcode.append(code)
                    stationlat.append(lat)
                    stationlon.append(lon)
                    stationelevation.append(elevation)
                    stationname.append(name)
                    stationcountry.append(country)
                    stationfirstyear.append(firstyear)
                    stationlastyear.append(lastyear)
            else:
                continue
    f.close

    # construct dataframe
    
    df = pd.DataFrame(columns=['year','1','2','3','4','5','6','7','8','9','10','11','12'])
    df['year'] = [ int(yearlist[i]) for i in range(len(yearlist)) ]

    for j in range(1,13):

        df[df.columns[j]] = [ monthlist[i][j-1] for i in range(len(monthlist)) ]

    df['stationcode'] = stationcode    
    df['stationlat'] = stationlat
    df['stationlon'] = stationlon
    df['stationelevation'] = stationelevation
    df['stationname'] = stationname
    df['stationcountry'] = stationcountry
    df['stationfirstyear'] = stationfirstyear
    df['stationlastyear'] = stationlastyear

    # trim strings
    
    df['stationname'] = [ str(df['stationname'][i]).strip() for i in range(len(df)) ] 
    df['stationcountry'] = [ str(df['stationcountry'][i]).strip() for i in range(len(df)) ] 

    # convert numeric variables from list of str to int (important due to fillValue)   
    
    for j in range(1,13):

        df[df.columns[j]] = df[df.columns[j]].astype('int')

    df['stationlat'] = df['stationlat'].astype('int')
    df['stationlon'] = df['stationlon'].astype('int')
    df['stationelevation'] = df['stationelevation'].astype('int')    
    df['stationfirstyear'] = df['stationfirstyear'].astype('int')    
    df['stationlastyear'] = df['stationlastyear'].astype('int')    
    
    # replace fill values in int variables:
            
    for j in range(1,13):

        df[df.columns[j]].replace(-9999, np.nan, inplace=True)

    df['stationlat'].replace(-9999, np.nan, inplace=True) 
    df['stationlon'].replace(-9999, np.nan, inplace=True) 
    df['stationelevation'].replace(-9999, np.nan, inplace=True) 
    df['stationfirstyear'].replace(-9999, np.nan, inplace=True) 
    df['stationlastyear'].replace(-9999, np.nan, inplace=True) 
                    
    return df

#------------------------------------------------------------------------------
# LOAD: CRU TS v4.04 --> df
#------------------------------------------------------------------------------

df= load_dataframe(filename_txt)
df.to_csv(filename_txt + '.csv')

#------------------------------------------------------------------------------
print('** END')




