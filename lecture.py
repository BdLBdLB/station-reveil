# -*- coding: utf-8 -*-
"""
Created on Mon May 23 10:26:12 2022

@author: benoit.delabatut
"""

import json
import requests
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TKAgg')
import pandas as pd
import numpy as np

import checktime

# %%
def getWeather(mode):
    """
    Executes two requests to get the current weather and the 4 days forecast in Paris
    mode: 0 uses already saved forecast (no actual request)
          1 requests 2 json from openweathermap.org

    return 2 json (weather and forecast)
    """
    if mode == 0: # use saved data
        forecast_data = json.load(open("forecast.json", "r"))
        weather_data = json.load(open("weather.json", "r"))

    else: # call API weatherforecastmap
        #todo Interroger l'API uniquement si la dernière requête est plus vieille que 10 minutes
        API_key = "ce386df03805fde750160dc2037f729c" # \todo Cacher cette clé     
        city_id = "2968815" # Paris : 2968815
        
        base_url_forecast = "http://api.openweathermap.org/data/2.5/forecast?" # forecast sur 4 jours - https://openweathermap.org/api/hourly-forecast#data
        Final_url_forecast = base_url_forecast + "appid=" + API_key + "&id=" + city_id
        
        base_url_weather = "http://api.openweathermap.org/data/2.5/weather?" # meteo actuelle - https://openweathermap.org/current
        Final_url_weather = base_url_weather + "appid=" + API_key + "&id=" + city_id
        
        try:
            weather_data = requests.get(Final_url_weather, timeout = 1).json()
            forecast_data = requests.get(Final_url_forecast, timeout = 1).json()
            
            # update the timestamp of the API as API responded
            lastOpenWeatherMapRequests = {"date" : str(datetime.now())}
            with open("lastOpenWeatherMapRequests.json", "w") as write_file:
                json.dump(lastOpenWeatherMapRequests, write_file)
                
            # update the last json 
            with open("weather.json", "w") as write_file:
                json.dump(weather_data, write_file)
            with open("forecast.json", "w") as write_file:
                json.dump(forecast_data, write_file)
            
        except: # \todo autoriser l'utilisation d'une ancienne requette si pas trop vieille
            weather_data = {}
            forecast_data = {}
            print("impossible d'interroger l'API open weather map")

    return weather_data, forecast_data

    
def extractForecast(weather_data, forecast_data):
    """
    reads 2 json to create 1 pandas dataframe with relevent information
    return 1 dataframe
    """
    # init du dataframe contenant toutes les prévisions
    previsions = pd.DataFrame(columns=['heureDePrediction','temperaturePrevue','temperatureRessentie','temperatureMinmale', 'temperatureMaximale', 'precipitations', 'icon'])

    # Lecture des donnees de la meteo actuelle
    try:
        heureDePrediction = datetime.fromtimestamp(weather_data["dt"])
    except:
        print("no timestamp !")
        heureDePrediction = np.nan
    try:
        temperaturePrevue = weather_data["main"]["temp"]-273.15
    except:
        temperaturePrevue = np.nan
    try:
            temperatureRessentie = weather_data["main"]["feels_like"]-273.15
    except:
            temperatureRessentie = np.nan
    try:
            temperatureMinmale = weather_data["main"]["temp_min"]-273.15
    except:
            temperatureMinmale = np.nan
    try:
            temperatureMaximale = weather_data["main"]["temp_max"]-273.15
    except:
            temperatureMaximale = np.nan
    try:
            precipitations = weather_data["rain"]["3h"]
    except:
            try:
                print(weather_data["rain"])
                print("erreur dans la lecture des précipitations")
            except:
                pass
            precipitations = 0
    try:
        icon = weather_data["weather"][0]["icon"]
    except:
        icon = ""
        
    # mise a jour du dataframe previsions  
    try:
        prevision = pd.DataFrame([[heureDePrediction, temperaturePrevue, temperatureRessentie, temperatureMinmale, temperatureMaximale, precipitations, icon]], columns=['heureDePrediction','temperaturePrevue','temperatureRessentie','temperatureMinmale', 'temperatureMaximale', 'precipitations', 'icon'])
        previsions = pd.concat([previsions, prevision], ignore_index = True)
    except:
        pass


    # lecture de la meteo des prochaines heures
    try:
        for forecast in forecast_data["list"]:
            try:
                heureDePrediction = datetime.fromtimestamp(forecast["dt"])
            except:
                print("pas de timestamp")
                heureDePrediction = np.nan
            try:
                temperaturePrevue = forecast["main"]["temp"]-273.15
            except:
                temperaturePrevue = np.nan
            try:
                temperatureRessentie = forecast["main"]["feels_like"]-273.15
            except:
                temperatureRessentie = np.nan
            try:
                temperatureMinmale = forecast["main"]["temp_min"]-273.15
            except:
                temperatureMinmale = np.nan
            try:
                temperatureMaximale = forecast["main"]["temp_max"]-273.15
            except:
                temperatureMaximale = np.nan
            try:
                precipitations = forecast["rain"]["3h"]
            except: 
                try: # \todo Comprendre la difference entre 3h et 1h
                    print(forecast["rain"])
                    print("erreur dans la lecture des précipitations")
                except:
                    pass
                precipitations = 0
            # \todo Ajouter les chutes de neige
            try:
                icon = forecast["weather"][0]["icon"]
            except:
                icon = ""
            
            # mise a jour du dataframe previsions   
            try:
                prevision = pd.DataFrame([[heureDePrediction, temperaturePrevue, temperatureRessentie, temperatureMinmale, temperatureMaximale, precipitations, icon]], columns=['heureDePrediction','temperaturePrevue','temperatureRessentie','temperatureMinmale', 'temperatureMaximale', 'precipitations', 'icon'])
                previsions = pd.concat([previsions, prevision], ignore_index = True)
            except:
                pass
    except: 
        print("aucun forecast")

    return previsions


def giveWeather():
    
    isWeatherOld = checktime.isWeatherOld()
    if isWeatherOld == 0:
        weather_data, forecast_data = getWeather(0)
    elif isWeatherOld == 1:
        weather_data, forecast_data = getWeather(1)

    previsions = extractForecast(weather_data, forecast_data)
    
    return previsions
 
if __name__ == '__main__':    
    previsions = giveWeather()      
 
    
    plt.figure()
    ax1 = plt.subplot(211)
    plt.plot(previsions["heureDePrediction"], previsions["temperaturePrevue"], label = "temperature prevue")
    plt.plot(previsions["heureDePrediction"], previsions["temperatureRessentie"], label = "temperature ressentie")
    # plt.plot(previsions["heureDePrediction"], previsions["temperatureMinmale"], label = "temperature minimale")
    # plt.plot(previsions["heureDePrediction"], previsions["temperatureMaximale"], label = "temperature maximale")
    plt.ylabel("°C")
    plt.grid(True)
    plt.box(True)
    plt.legend()
    
    plt.subplot(212, sharex = ax1)
    plt.plot(previsions["heureDePrediction"], previsions["precipitations"])
    plt.ylabel('Précipitations [mm]')
    plt.box(True)
    plt.grid(True)
    plt.show()

# # %%
# icon = weather_data["weather"][0]["icon"]
# url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
# #img = plt.imread("http://openweathermap.org/img/wn/10d@2x.png")
# img = plt.imread(url)
# plt.figure()
# plt.imshow(img)
# plt.box(False)










