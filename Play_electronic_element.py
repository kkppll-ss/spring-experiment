# -*- coding: UTF-8 -*-

import time
import threading
import random
import pygame,sys


# clip = mp3play.load("sound/capacitor.mp3")
# clip.play()
# time.sleep(10)
# clip.stop()


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
        # self.set_label = set_Position_label

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_mode([1, 1])

    def run(self):
        while self.stop is False:
            self.currentElectronicElement = random.randrange(1, 6)
            self.traceList.append(self.currentElectronicElement)
            # clip = mp3play.load("sound/"+self.sound_list[self.currentElectronicElement - 1]+".mp3")
            # clip.play()
            # time.sleep(2)
            # clip.stop()
            pygame.time.delay(3000)
            pygame.mixer.music.load("sound/"+self.sound_list[self.currentElectronicElement - 1]+".mp3")
            pygame.mixer.music.play()

            # self.set_label(self.currentElectronicElement)

    def terminate(self, stop=1):
        if stop == 1:
            self.stop = True

    def last_i_th(self, last_i_th):
        # if last_i_th > len(self.traceList):
        #     last_i_th = 1
        return self.traceList[-last_i_th]


# music_play = play_electronic_element()
# music_play.start()
# a = int(raw_input())
# music_play.terminate(a)
# print "The last 2 electronic element hear of: " + str(music_play.last_i_th(2))
# print music_play.traceList

#
# # print "The Last element" + str(music_play.currentElectronicElement + 1)
# print "Hello all sound terminated"



