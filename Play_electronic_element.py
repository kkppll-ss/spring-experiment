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

    def run(self):
        while self.stop is False:
            self.currentElectronicElement = random.randrange(0, 100)
            self.traceList.append(self.currentElectronicElement)
            p = vlc.MediaPlayer("sound/" + str(self.currentElectronicElement) + ".mp3")
            p.play()
            time.sleep(1)
            p.stop()

    def terminate(self, stop=1):
        if stop == 1:
            self.stop = True

    def last_i_th(self, last_i_th):
        return self.traceList[-last_i_th]


if __name__ == "__main__":
    music_play = play_electronic_element()
    music_play.start()
