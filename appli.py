# importing required librarie
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer, QTime, Qt

# from pyqtgraph import PlotWidget, plot # pip install pyqtgraph==0.11.1
# import pyqtgraph as pg

import pandas as pd
import numpy as np
from datetime import datetime

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


import getWeather
import Weather
import date

  
  
class Window(QWidget):
  
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 800)
        layout = QVBoxLayout()
        self.setLayout(layout)
        font = QFont('Arial', 120, QFont.Bold)
        self.setStyleSheet("background-color: green;") 

        # creating a label object for the clock
        self.labelClock = QLabel() 
        self.labelClock.setAlignment(Qt.AlignCenter)  
        self.labelClock.setFont(font) 
        layout.addWidget(self.labelClock) 
        timerClock = QTimer(self)  
        timerClock.timeout.connect(self.showTime) 
        timerClock.start(1000)     
        
        # creating a label for the day
        self.labelDay = QLabel()
        self.labelDay.setAlignment(Qt.AlignCenter)
        self.labelDay.setFont(QFont('Arial', 20))
        # self.labelDay.setText(date.todayAsAString())
        layout.addWidget(self.labelDay) 


        layoutWeather = QHBoxLayout()
        layout.addLayout(layoutWeather)
        
        layoutInfoWeather = QVBoxLayout()
        layoutWeather.addLayout(layoutInfoWeather)
        
        # creating a label for the weather
        self.labelWeather = QLabel()
        self.labelWeather.setAlignment(Qt.AlignCenter)  
        self.labelWeather.setFont(QFont('Arial', 10)) 
        #self.labelWeather.setText(getWeather.getWeather())
        layoutInfoWeather.addWidget(self.labelWeather)
        timerWeather = QTimer(self)  
        timerWeather.timeout.connect(self.showWeather) 
        timerWeather.start(1000*60*5) # actualisation de la meteo toutes les 5 minutes     
        
        # creating a label for the weather icon
        self.labelIconWeather = QLabel(self)
        # pixmap = QPixmap(weather.loadWeatherIcon(0))
        # self.labelIconWeather.setPixmap(pixmap)
        layoutInfoWeather.addWidget(self.labelIconWeather)
        self.labelIconWeather.setAlignment(Qt.AlignCenter)  
                
        # --- plot
        layoutPlot = QVBoxLayout()
        layoutWeather.addLayout(layoutPlot)
        
        self.figure = Figure()
        self.axisTemperature = self.figure.add_subplot(211)  
        self.axisRain = self.figure.add_subplot(212, sharex = self.axisTemperature)

        self.canvas = FigureCanvas(self.figure)
        layoutPlot.addWidget(self.canvas)
        # ---
        
        self.showWeather()
        
        



  
    def showTime(self):  
        current_time = QTime.currentTime()  
        label_time = current_time.toString('hh:mm:ss') 
        self.labelClock.setText(label_time)
        
        self.labelDay.setText(date.todayAsAString()) # \todo effectuer cette action uniquement si changement de jour
    
    def showWeather(self):
        self.labelWeather.setText(getWeather.getWeather())
        
        weather.updatePrevisions()
        
        pixmap = QPixmap(weather.loadWeatherIcon(0))
        self.labelIconWeather.setPixmap(pixmap)
        
        
        self.axisTemperature.clear()
        self.axisTemperature.set_ylabel('Temperature (°C)')
        self.axisTemperature.plot(weather.previsions["heureDePrediction"], weather.previsions["temperaturePrevue"])
        
        self.axisRain.clear()
        self.axisRain.set_ylabel('Précipitations (mm)')
        self.axisRain.plot(weather.previsions["heureDePrediction"], weather.previsions["precipitations"])
        
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
# start the app
App.exit(App.exec_())