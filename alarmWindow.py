# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 21:11:45 2022

@author: benoit.delabatut
"""
#import sys
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt

import music


class Window(QWidget):
  
    def __init__(self):
        super().__init__()
        self.isOn = True
        self.setGeometry(100, 100, 800, 800)
        self.font = "Arial"
        self.fontColor = "white"
        self.setStyleSheet("background-color: black")
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.label = QLabel()
        self.label.setStyleSheet("color : " + self.fontColor)
        self.label.setAlignment(Qt.AlignCenter)  
        self.label.setFont(QFont(self.font, 20, QFont.Bold))
        self.label.setText("Bonne journée Benoît !")
        self.layout.addWidget(self.label) 
        
        self.button = QPushButton()
        self.button.setText("Button1")
        self.button.setStyleSheet("color : " + self.fontColor) 
        self.button.setFont(QFont(self.font, 20, QFont.Bold))
        self.button.setText("Debout")
        self.button.clicked.connect(self.buttonClicked)
        self.layout.addWidget(self.button)
        
        self.music = music.MorningMusic("ringtone/ringing_old_phone.wav")
        
        timer = QTimer(self)  
        timer.timeout.connect(self.musicLoop) # actualisation de la date/heure toutes les 2 secondes
        timer.start(2000) 
        
    def buttonClicked(self):
        self.music.stopMusic()
        self.isOn = False
        self.close()
        
        
    def musicLoop(self):
        if self.isOn == True:
            self.music.repeatMusic()
    
if __name__ == '__main__':
   win = Window()
   win.show() 