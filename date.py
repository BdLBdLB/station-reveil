# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from datetime import datetime

def todayAsAString():
    joursDeLaSemaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    moisDeLAnnee = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    
    date = joursDeLaSemaine[datetime.today().weekday()]
    date += " " + str(datetime.today().day)
    date += " " + moisDeLAnnee[datetime.today().month]
    date += " " + str(datetime.today().year)

    return date

def dayOfTheWeek(date):
    joursDeLaSemaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"] # \todo param global
    
    day = [] 
    for d in range(0, len(date)):
        day.append(25*" " + joursDeLaSemaine[date[d].weekday()])

    return day


