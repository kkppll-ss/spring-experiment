# -*- coding: UTF-8 -*-

import time
import threading
import random
import vlc


class play_electronic_element(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False
        self.currentElectronicElement = -1
        self.traceList = []
        # self.set_label = set_Position_label
        
    def run(self):
        while self.stop is False:
            self.currentElectronicElement = random.randrange(1, 10)
            self.traceList.append(self.currentElectronicElement)
            p = vlc.MediaPlayer("sound/" + "0" + str(self.currentElectronicElement) + ".mp3")
            p.play()
            time.sleep(2)
            p.stop()

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



