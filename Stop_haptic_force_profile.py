# -*- coding: UTF-8 -*-

import threading
import time


class Stop_haptic_force_profile(threading.Thread):

    def __init__(self, Experiment_Session):
        threading.Thread.__init__(self)
        self.Spring_GUI = Experiment_Session
        self.pre = 0
        self.cur = 0
        # self.num = 4

    def run(self):
        while True:
            # while self.num != 0:
            #     self.Spring_GUI.Position_Info.set(str(self.num))
            #     time.sleep(1)
            #     self.num -= 1
            #     if self.num == 0:
            #         self.num = 4

            if int(self.Spring_GUI.Position_Info.get()) == 0:
                if self.pre != 0:
                    # Stop the movement of Haptic Spring
                    # self.Spring_GUI.spring.terminate()

                    # Stop play the sound of electronic element
                    if self.Spring_GUI.currentTrial[1] == '1':
                        self.Spring_GUI.play_electronic_element.terminate()
                        self.Spring_GUI.trackLength = len(self.Spring_GUI.play_electronic_element.traceList)

                    self.Spring_GUI.deltatime = int(round(time.time() * 1000)) - self.Spring_GUI.start
                    self.Spring_GUI.Question_text.set("Haptic Test END")
                    self.Spring_GUI.Question.place(x=7 * self.Spring_GUI.width / 16, y=3 * self.Spring_GUI.height / 4)
                    self.Spring_GUI.Question.config(fg="red", font=("Courier", 23, "bold"))
                    self.Spring_GUI.Question.after(500, lambda: self.Spring_GUI.Question_text.set(""))

                    self.Spring_GUI.Question.after(500, lambda: self.Spring_GUI.Question_text.set("Select a Haptic Feel"))
                    self.Spring_GUI.Question.place(x=5 * self.Spring_GUI.width / 16, y=3 * self.Spring_GUI.height / 4)
                    self.Spring_GUI.Question.config(font=("Courier", 23, "bold"), fg="blue")
                    self.Spring_GUI.PressSpaceTwice = True
            else:
                self.pre = self.cur
                self.cur = self.Spring_GUI.Position_Info.get()

