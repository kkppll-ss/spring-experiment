# -*- coding: UTF-8 -*-

import time
import threading
import random
import pygame


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

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_mode([1, 1])

    def run(self):
        while self.stop is False:
            self.currentElectronicElement = random.randrange(1, 7)
            self.traceList.append(self.currentElectronicElement)
            pygame.mixer.music.load("sound/" + self.sound_list[self.currentElectronicElement - 1] + ".mp3")
            pygame.mixer.music.play()
            pygame.time.delay(2000)

    def terminate(self, stop=1):
        if stop == 1:
            self.stop = True

    def last_i_th(self, last_i_th):
        # if last_i_th > len(self.traceList):
        #     last_i_th = 1
        return self.traceList[-last_i_th]


if __name__ == "__main__":
    music_play = play_electronic_element()
    music_play.start()
    # a = int(raw_input())
    # music_play.terminate(a)
    # print "The last 2 electronic element hear of: " + str(music_play.last_i_th(2))
    # print music_play.traceList



