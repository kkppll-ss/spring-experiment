# -*- coding: UTF-8 -*-

import threading
import random
from playsound import playsound
import time


class play_electronic_element(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False
        self.currentElectronicElement = -1
        self.traceList = []
        self.sound_list = [
                              'capacitor',
                              'diode',
                              'Integrate Circuit',
                              'LED',
                              'resistor',
                              'transistor'
                            ]

    def run(self):
        while self.stop is False:
            self.currentElectronicElement = random.randrange(1, 6)
            self.traceList.append(self.currentElectronicElement)
            playsound("sound/"+self.sound_list[self.currentElectronicElement - 1]+".mp3")
            time.sleep(1)

    def terminate(self, stop=1):
        if stop == 1:
            self.stop = True

    def last_i_th(self, last_i_th):
        return self.traceList[-last_i_th]


# music_play = play_electronic_element()
# music_play.start()
# a = int(raw_input())
# music_play.terminate(a)
# print "The last 2 electronic element hear of: " + str(music_play.last_i_th(2))
# print music_play.traceList

# print "The Last element" + str(music_play.currentElectronicElement + 1)
# print "Hello all sound terminated"



