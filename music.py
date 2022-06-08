# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 20:02:56 2022

@author: benoit.delabatut
"""
# from playsound import playsound # lame
import simpleaudio as sa
import time

class MorningMusic:
    """
    Init the tune and starts playing it
    """
    def __init__(self, ringtone):
        self.wave_obj = sa.WaveObject.from_wave_file(ringtone)
        self.play_obj = self.wave_obj.play()
        
    def stopMusic(self):
        self.play_obj.stop()

    def repeatMusic(self):
        """
        Repeat the tunes if it is finished
        """
        if self.play_obj.is_playing():
            #print("still playing")
            pass
        else:
            #print("again !")
            self.play_obj = self.wave_obj.play()


if __name__ == '__main__':
    ringtone = "ringtone/ringing_old_phone.wav" # https://www.freeconvert.com/mp3-to-wav
    wave_obj = sa.WaveObject.from_wave_file(ringtone)
    play_obj = wave_obj.play()
    while 1:
        if play_obj.is_playing():
            print("still playing")
        else:
            print("again !")
            play_obj = wave_obj.play()
        time.sleep(2)
                
            
    play_obj.stop()
    play_obj.wait_done()

    