# -*- coding: utf-8 -*-
"""
Created on Tue May 24 08:37:41 2022

@author: benoit.delabatut
"""

import json
from datetime import datetime, timedelta


# %%
def isWeatherOld():
    """
    checks timestamp to see if weather forecast is outdated
    return isWeatherOld :
        0: forecast is not outdated and API should not be interrogated
        1: forecast is outdated and API may be interrogated
    """
    format = "%Y-%m-%d %H:%M:%S.%f"
    openWeatherMapExpirationDuration = 60 * 15 # \todo parametre global
    
    try : # read the time stamp of the last succesful API request
        with open("lastOpenWeatherMapRequests.json", "r") as read_file:
            lastOpenWeatherMapRequests = json.load(read_file)
        
    except: # initialize time stamp if API never responded
        lastOpenWeatherMapRequests = {"date" : str(datetime.now() - timedelta(seconds = openWeatherMapExpirationDuration + 1))}
        with open("lastOpenWeatherMapRequests.json", "w") as write_file:
            json.dump(lastOpenWeatherMapRequests, write_file)
           
    lastOpenWeatherMapRequests_date = datetime.strptime(lastOpenWeatherMapRequests["date"], format)
    lastOpenWeatherMapRequests_dateExpiration = lastOpenWeatherMapRequests_date + timedelta(seconds = openWeatherMapExpirationDuration)
         
    if datetime.now() < lastOpenWeatherMapRequests_dateExpiration: # to early to call API
        #print("to early to call API")
        isWeatherOld = 0
    
    else: # API can be called
        #print("API can be called") # fonction d'appel de l'API + creation des json
        isWeatherOld = 1
        
    return isWeatherOld



