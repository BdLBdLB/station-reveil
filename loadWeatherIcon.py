# -*- coding: utf-8 -*-
"""
Created on Tue May 24 19:00:04 2022

@author: benoit.delabatut
"""
import requests
from PIL import Image
import pandas as pd
import numpy as np
from datetime import datetime

import lecture

def loadWeatherIcon():
    """
    fetch current weather icon
    return iconURL:
        URL of the icon 
    """
    previsions = lecture.giveWeather()    
    iconID = previsions["icon"][0]

    try: 
        # Icon is already saved
        icon = open("icon/" + iconID + ".png")
        print("l'icone existe deja")
    except:
        # icon is downloaded from openweathermap
        url = "http://openweathermap.org/img/wn/" + iconID + "@2x.png"
        #img = plt.imread("http://openweathermap.org/img/wn/10d@2x.png")
        try:
            icon = Image.open(requests.get(url, stream=True).raw)
            icon.save("icon/" + iconID + ".png")
            icon = open("icon/" + iconID + ".png")
            print("l'icone n'existe pas mais a ete telechargée")
        except:
            print("impossible de telecharger l'icon :(")
            # \todo : trouver une icone par defaut
            
    return previsions, "icon/" + iconID + ".png"    
        
    