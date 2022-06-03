# importing required librarie
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QLabel
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer, QTime, Qt

# from pyqtgraph import PlotWidget, plot # pip install pyqtgraph==0.11.1
# import pyqtgraph as pg

# import pandas as pd
import numpy as np
# from datetime import datetime

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates


import Weather
import date
import alarm

  
  
class Window(QWidget):
  
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 800)
        font = "Arial"
        fontColor = "white"
        self.setStyleSheet("background-color: black")
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        # creating a label object for the clock
        self.labelClock = QLabel() 
        self.labelClock.setStyleSheet("color : " + fontColor)
        self.labelClock.setAlignment(Qt.AlignCenter)  
        self.labelClock.setFont(QFont(font, 120, QFont.Bold))
        layout.addWidget(self.labelClock)     
        
        # creating a label to display alarm time
        self.labelAlarm = QLabel() 
        self.labelAlarm.setStyleSheet("color : " + fontColor)
        self.labelAlarm.setAlignment(Qt.AlignCenter)  
        self.labelAlarm.setFont(QFont(font, 15, QFont.Bold))
        layout.addWidget(self.labelAlarm) 
        
        # creating a label for the day
        self.labelDay = QLabel()
        self.labelDay.setStyleSheet("color : " + fontColor)
        self.labelDay.setAlignment(Qt.AlignCenter)
        self.labelDay.setFont(QFont(font, 20))
        layout.addWidget(self.labelDay) 


        layoutWeather = QHBoxLayout()
        layout.addLayout(layoutWeather)
        
        # create a layout for icon and temperature
        layoutCloseWeather = QGridLayout()
        layoutWeather.addLayout(layoutCloseWeather)
        
        
        self.labelIconWeather0 = QLabel(self)
        layoutCloseWeather.addWidget(self.labelIconWeather0, 0, 0)
        self.labelIconWeather0.setAlignment(Qt.AlignCenter) 
        self.labelIconWeather1 = QLabel(self)
        layoutCloseWeather.addWidget(self.labelIconWeather1, 0, 1)
        self.labelIconWeather1.setAlignment(Qt.AlignCenter) 
        self.labelIconWeather2 = QLabel(self)
        layoutCloseWeather.addWidget(self.labelIconWeather2, 0, 2)
        self.labelIconWeather2.setAlignment(Qt.AlignCenter) 
        
        self.Temperature0 = QLabel()
        self.Temperature0.setStyleSheet("color : " + fontColor)
        self.Temperature0.setAlignment(Qt.AlignHCenter)
        self.Temperature0.setFont(QFont(font, 30))
        layoutCloseWeather.addWidget(self.Temperature0, 1, 0) 
        self.Temperature1 = QLabel()
        self.Temperature1.setStyleSheet("color : " + fontColor)
        self.Temperature1.setAlignment(Qt.AlignHCenter)
        self.Temperature1.setFont(QFont(font, 30))
        layoutCloseWeather.addWidget(self.Temperature1, 1, 1) 
        self.Temperature2 = QLabel()
        self.Temperature2.setStyleSheet("color : " + fontColor)
        self.Temperature2.setAlignment(Qt.AlignHCenter)
        self.Temperature2.setFont(QFont(font, 30))
        layoutCloseWeather.addWidget(self.Temperature2, 1, 2) 
        
         
                
        # --- plot 
        plt.style.use("seaborn-dark")            
            
        self.figure = Figure()
        matplotlib.rcParams['font.family'] = font
        matplotlib.rcParams['text.color'] = fontColor
        matplotlib.rcParams['axes.labelcolor'] = fontColor
        matplotlib.rcParams['xtick.color'] = fontColor
        matplotlib.rcParams['ytick.color'] = fontColor
        plt.rc('font', size=15)
        self.figure.patch.set_alpha(0)
        
        self.axisTemperature = self.figure.add_subplot(211)  
        self.axisRain = self.figure.add_subplot(212, sharex = self.axisTemperature)
        self.canvas = FigureCanvas(self.figure)
        layoutWeather.addWidget(self.canvas)
        # ---
        
        
        timerClock = QTimer(self)  
        timerClock.timeout.connect(self.showTime) # actualisation de la date/heure toutes les secondes
        timerClock.start(1000) 
        
        timerWeather = QTimer(self)  
        timerWeather.timeout.connect(self.showWeather) 
        timerWeather.start(1000*60*5) # actualisation de la meteo toutes les 5 minutes     
        
        self.showWeather()
        
        



  
    def showTime(self):  
        current_time = QTime.currentTime()  
        label_time = current_time.toString('hh:mm:ss') 
        self.labelClock.setText(label_time)
        
        alarmTime = alarm.getAlarmTime()
        self.labelAlarm.setText("(" + str(alarmTime["hour"]) + ":" + str(alarmTime["minute"]) + ")")
        
        if alarm.isItTime(alarmTime) and alarm.isAlarmOn():
            print("ding dong")
            window2 = Window()  
            # showing all the widgets
            window2.show()  
        
        self.labelDay.setText(date.todayAsAString()) # \todo effectuer cette action uniquement si changement de jour
    
    def showWeather(self):
               
        weather.updatePrevisions()
        
        pixmap = QPixmap(weather.loadWeatherIcon(0))
        self.labelIconWeather0.setPixmap(pixmap)
        pixmap = QPixmap(weather.loadWeatherIcon(1)) # \todo si forecast 1 trop proche de 0, afficher icone 2 et 3
        self.labelIconWeather1.setPixmap(pixmap)
        pixmap = QPixmap(weather.loadWeatherIcon(2))
        self.labelIconWeather2.setPixmap(pixmap)
        
        self.Temperature0.setText(str(round(weather.previsions["temperaturePrevue"][0], 1)) + "°C")
        self.Temperature1.setText(str(round(weather.previsions["temperaturePrevue"][1], 1)) + "°C")
        self.Temperature2.setText(str(round(weather.previsions["temperaturePrevue"][2], 1)) + "°C")
        
        
        self.axisTemperature.clear()
        self.axisTemperature.set_ylabel('Temperature (°C)')
        
        self.axisRain.clear()
        self.axisRain.set_ylabel('Précipitations (mm)')
        
        n_lines = 10
        diff_linewidth = 1.05
        alpha_value = 0.03
        self.axisRain.bar(weather.previsions["heureDePrediction"], weather.previsions["precipitations"], width = 0.12, color = 'b')
        self.axisTemperature.plot(weather.previsions["heureDePrediction"], weather.previsions["temperaturePrevue"], marker = "o", color = '#FE53BB')
        for n in range(1, n_lines+1):
            self.axisTemperature.plot(weather.previsions["heureDePrediction"], weather.previsions["temperaturePrevue"], 
                               marker = "o", 
                               linewidth=2+(diff_linewidth*n), 
                               alpha=alpha_value,                                      
                               color = '#FE53BB')
            
        self.axisTemperature.fill_between(weather.previsions["heureDePrediction"], weather.previsions["temperaturePrevue"], color = "#FE53BB", alpha = 0.2)
                  
        self.axisTemperature.set_xlim(min(weather.previsions["heureDePrediction"]), max(weather.previsions["heureDePrediction"]))
        self.axisTemperature.grid(color='#2A3459')
        self.axisRain.grid(color='#2A3459')

        self.axisTemperature.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
        
        self.axisRain.patch.set_alpha(0)
        self.axisTemperature.patch.set_alpha(0)
        
        self.axisRain.set_xlim(np.min(weather.previsions["heureDePrediction"].apply(lambda x : x)), np.max(weather.previsions["heureDePrediction"].apply(lambda x : x)))
        xticks = list(set(weather.previsions["heureDePrediction"].apply(lambda x : x.replace(hour = 0))))
        self.axisRain.set(xticks = xticks)
        self.axisRain.set(xticklabels = date.dayOfTheWeek(xticks))

        self.axisTemperature.set_xlim(np.min(weather.previsions["heureDePrediction"].apply(lambda x : x)), np.max(weather.previsions["heureDePrediction"].apply(lambda x : x)))
        
        
        # --
        self.axisTemperature.grid(color='#2A3459')
        self.axisRain.grid(color='#2A3459')
        #--
        
        self.figure.tight_layout() 
        self.axisTemperature.figure.canvas.draw()
        self.axisRain.figure.canvas.draw()
        


  
# create pyqt5 app
weather = Weather.Weather()
App = QApplication(sys.argv)  
# create the instance of our Window
window = Window()  
# showing all the widgets
window.show()  
# window.showFullScreen()
# start the App
# sys.exit()
App.exit(App.exec_())