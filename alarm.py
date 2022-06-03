# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 23:00:34 2022

@author: benoit.delabatut
"""
from datetime import datetime, timedelta
import time

def getAlarmTime():
    """
    Return the alarm time
    \todo get alarm time from database
    """
    alarmTime = {
        "hour": 0,
        "minute": 4,
        "second": 0}
    
    return alarmTime

def isAlarmOn():
    """
    Return True if alarm is set
           False if alarm is not set 
    \todo get alarm confirmation from database
    """
    AlarmOn = True
    
    return AlarmOn

def isItTime(alarmTime):
    """
    Checks if alarm should be rung
    
    return True if it is time
    """
    itIsTime = False
    currentTime = datetime.now()
    if alarmTime["hour"] == currentTime.hour and alarmTime["minute"] == currentTime.minute and alarmTime["second"] == currentTime.second:
        itIsTime = True
    
    return itIsTime


if __name__ == '__main__':
    import time
    alarm = getAlarmTime()
    isAlarmOn = isAlarmOn()
    
    # ringing = False
    # while 1:
    #     if (datetime.now()- alarm).seconds < 5 and (datetime.now()- alarm).seconds > 0: # 5 sec period after the alarm time
    #         if ringing == False:
    #             print("ding dong")
    #             ringing = True
    #         else:
    #             print("already started")
    #     else:
    #         print(datetime.now())
    #     time.sleep(0.5)
    
# %%