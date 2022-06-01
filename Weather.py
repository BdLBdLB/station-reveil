# -*- coding: utf-8 -*-
"""
Created on Wed May 25 08:40:53 2022

@author: benoit.delabatut
"""
import json
import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from PIL import Image



class Weather():
    """
    """
    openWeatherMapExpirationDuration = 60 * 15 # \todo parametre global
    format = "%Y-%m-%d %H:%M:%S.%f"  
    
    def __init__(self):              
        self.timestamp = self.initializeTimeStamp()
        
        weather_data, forecast_data = self.getWeather(self.isWeatherOld())
        self.previsions = self.extractForecast(weather_data, forecast_data)
        
        
    def updatePrevisions(self):
        """
        update previsions if necessary

        """
        if self.isWeatherOld() == 1:
            weather_data, forecast_data = self.getWeather(1)
            self.previsions = self.extractForecast(weather_data, forecast_data)
        
        
    def getWeather(self, mode):
        """
        Executes two requests to get the current weather and the 4 days forecast in Paris
        mode: 
            0 uses already saved forecast (no actual request)
            1 requests 2 json from openweathermap.org
    
        return 2 json (weather and forecast)
        """
        if mode == 0: # use saved data
            forecast_data = json.load(open("forecast.json", "r"))
            weather_data = json.load(open("weather.json", "r"))
    
        else: # call API weatherforecastmap
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
                    
                self.timestamp = datetime.strptime(lastOpenWeatherMapRequests["date"], self.format)
                
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
    

    def extractForecast(self, weather_data, forecast_data):
        """
        reads 2 json to create 1 pandas dataframe with relevent information
        return 1 dataframe
        """
        # initialisation
        previsions = pd.DataFrame(columns=['heureDePrediction','temperaturePrevue','temperatureRessentie','temperatureMinmale', 'temperatureMaximale', 'precipitations', 'icon'])
    
        # Read data of current weather
        try:
            heureDePrediction = datetime.fromtimestamp(weather_data["dt"]) # https://www.epochconverter.com/
            #print(heureDePrediction)
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
            
        # update dateframe with current weather  
        try:
            prevision = pd.DataFrame([[heureDePrediction, temperaturePrevue, temperatureRessentie, temperatureMinmale, temperatureMaximale, precipitations, icon]], columns=['heureDePrediction','temperaturePrevue','temperatureRessentie','temperatureMinmale', 'temperatureMaximale', 'precipitations', 'icon'])
            previsions = pd.concat([previsions, prevision], ignore_index = True)
        except:
            pass
    
    
        # Read data of forecasts
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
                
                # update previsions with forecast   
                try:
                    prevision = pd.DataFrame([[heureDePrediction, temperaturePrevue, temperatureRessentie, temperatureMinmale, temperatureMaximale, precipitations, icon]], columns=['heureDePrediction','temperaturePrevue','temperatureRessentie','temperatureMinmale', 'temperatureMaximale', 'precipitations', 'icon'])
                    previsions = pd.concat([previsions, prevision], ignore_index = True)
                except:
                    pass
        except: 
            print("aucun forecast")
    
        return previsions
    
    
    def isWeatherOld(self):
        """
        checks timestamp to see if weather forecast is outdated
        return isWeatherOld :
            0: forecast is not outdated and API should not be interrogated
            1: forecast is outdated and API may be interrogated
        """
               
        lastOpenWeatherMapRequests_dateExpiration = self.timestamp + timedelta(seconds = self.openWeatherMapExpirationDuration)
        
        
        if datetime.now() < lastOpenWeatherMapRequests_dateExpiration: # to early to call API
            # print("to early to call API")
            isWeatherOld = 0
        
        else: # API can be called
            # print("API can be called") # fonction d'appel de l'API + creation des json
            isWeatherOld = 1
            
        return isWeatherOld
    
    
    def initializeTimeStamp(self):
        """
        sets self.timestamp and save it into a Json
        """
        
        try : # read the time stamp of the last succesful API request
            with open("lastOpenWeatherMapRequests.json", "r") as read_file:
                lastOpenWeatherMapRequests = json.load(read_file)

            
        except: # initialize time stamp if API never responded
            lastOpenWeatherMapRequests = {"date" : str(datetime.now() - timedelta(seconds = self.openWeatherMapExpirationDuration + 1))}
            with open("lastOpenWeatherMapRequests.json", "w") as write_file:
                json.dump(lastOpenWeatherMapRequests, write_file)
        
        timestamp = datetime.strptime(lastOpenWeatherMapRequests["date"], self.format)
        
        return timestamp
    
    
    def loadWeatherIcon(self, i):
        """
        fetch weather icon i 
            i = 0: current weather
        return iconURL:
            URL of the icon 
        """
        iconID = self.previsions["icon"][i]
    
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
                
        return "icon/" + iconID + ".png"   
    
    
if __name__ == '__main__':  
    from matplotlib import pyplot as plt
    import matplotlib
    matplotlib.use('TKAgg')
    import matplotlib.dates as mdates
    
    import date
    
    we = Weather()
    
    figure = plt.figure()
    figure.clear()
    ax1 = plt.subplot(211)
    plt.plot(we.previsions["heureDePrediction"], we.previsions["temperaturePrevue"], label = "temperature prevue")
    plt.plot(we.previsions["heureDePrediction"], we.previsions["temperatureRessentie"], label = "temperature ressentie")
    # plt.plot(we.previsions["heureDePrediction"], we.previsions["temperatureMinmale"], label = "temperature minimale")
    # plt.plot(we.previsions["heureDePrediction"], we.previsions["temperatureMaximale"], label = "temperature maximale")
    plt.ylabel("°C")
    plt.grid(True)
    plt.box(True)
    plt.legend()
    
    ax2 = plt.subplot(212, sharex = ax1)
    plt.bar(we.previsions["heureDePrediction"], we.previsions["precipitations"], width = 0.12)
    plt.ylabel('Précipitations [mm]')
    plt.box(True)
    plt.grid(True)
    plt.show()
    
    ax2.set_xlim(np.min(we.previsions["heureDePrediction"].apply(lambda x : x)), np.max(we.previsions["heureDePrediction"].apply(lambda x : x)))
    xticks = list(set(we.previsions["heureDePrediction"].apply(lambda x : x.replace(hour = 0))))
    xtickslabel = date.dayOfTheWeek(xticks)
    ax2.set(xticks = xticks)
    ax2.set(xticklabels = xtickslabel)
    
    ax1.set_xlim(np.min(we.previsions["heureDePrediction"].apply(lambda x : x)), np.max(we.previsions["heureDePrediction"].apply(lambda x : x)))
    # ax1.set(xticks = xticks)
    # ax1.set(xticklabels = date.dayOfTheWeek(xticks))
    
# %% 
    
    # # %%
    # icon = weather_data["weather"][0]["icon"]
    # url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
    # #img = plt.imread("http://openweathermap.org/img/wn/10d@2x.png")
    # img = plt.imread(url)
    # plt.figure()
    # plt.imshow(img)
    # plt.box(False)