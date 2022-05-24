#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from pushbullet import Pushbullet
import json
import urllib.request
import datetime

#PB_API_KEY = ""
OWM_API_KEY = "ce386df03805fde750160dc2037f729c"
CITY = "Paris"
NOTIF_TITLE = "Météo du jour"
#DEVICE_ID = ""; # Send to specific device (run print(pb.devices) to get key)
OWM_API_BASE_URL = "http://api.openweathermap.org/data/2.5/"


def getWeather():
    content = ""

    weather_gps = json.loads(urllib.request.urlopen(OWM_API_BASE_URL+"weather?APPID="+OWM_API_KEY+"&q="+urllib.parse.quote_plus(CITY.encode("utf8"))+"&mode=json&units=metric").read())

    if 'lon' in weather_gps['coord']:
        gps_lon = str(weather_gps['coord']['lon'])
        gps_lat = str(weather_gps['coord']['lat'])

        weather = json.loads(urllib.request.urlopen(OWM_API_BASE_URL+"onecall?APPID="+OWM_API_KEY+"&lat="+gps_lat+"&lon="+gps_lon+"&units=metric&lang=fr&exclude=hourly").read())
        
        # print(weather)
        
        if 'current' in weather:
            current_temp = str(weather['current']['temp'])
            current_temp_feels = str(weather['current']['feels_like'])
            weather_desc = str(weather['current']['weather'][0]['description'])
            day_max_temp =  str(weather['daily'][0]['temp']['max'])
            
            content = "Il fait actuellement "+current_temp+"°C ("+current_temp_feels+"°C ressenti) à "+CITY+"."
            content += "\n"
            content += "Le temps est "+weather_desc+"."
            content += "\n"
            content += "La maximale sera de "+day_max_temp+"°C."
            content += "\n"
            content += str(datetime.datetime.now())
    
    return content;


getWeather()