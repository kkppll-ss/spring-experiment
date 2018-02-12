# -*- coding: UTF-8 -*-

import time
import Image
import Tkinter
import ImageTk
import tkMessageBox
import Produce_Read_Order_List

from Tkinter import *
from Spring import Spring


class Experiment_Session:

    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title("Haptic Experiment")
        self.center_window(self.root, 600, 600)
        self.root.maxsize(800, 600)
        self.root.minsize(300, 240)

        # Bind the Space Key press to continue
        self.root.bind("<KeyPress>", self.SpaceContinue)
        self.root.focus_set()
        self.root.bind('<Return>', self.EnterPress)
        self.spring = Spring()

        self.cmd = Produce_Read_Order_List.Produce_Read_Order_List()
        self. cmd.make_pairs()
        self.User_feel_FP = -1               # record the user's actual choice of haptic feeling
        self.User_enter_feel = ""
        self.global_times_counter = 0        # record the user's repeated times
        self.start = 0
        self.end = 0
        self.deltatime = 0

        self.varNum = Tkinter.StringVar(value='')
        self.varName = Tkinter.StringVar(value='')
        self.varGender = Tkinter.StringVar(value='')
        self.varAge = Tkinter.StringVar(value='')

        self.labelNum = Tkinter.Label(self.root, text='User Num:')
        self.labelNum.place(x=10, y=5, width=80, height=20)
        self.entryNum = Tkinter.Entry(self.root, width=80, textvariable=self.varNum)
        self.entryNum.place(x=100, y=5, width=80, height=20)

        self.LabelName = Tkinter.Label(self.root, text='Name:')
        self.LabelName.place(x=10, y=30, width=80, height=20)
        self.entryName = Tkinter.Entry(self.root, width=80, textvariable=self.varName)
        self.entryName.place(x=100, y=30, width=80, height=20)

        self.LabelGender = Tkinter.Label(self.root, text='Gender:')
        self.LabelGender.place(x=170, y=5, width=80, height=20)
        self.entryGender = Tkinter.Entry(self.root, width=80, textvariable=self.varGender)
        self.entryGender.place(x=270, y=5, width=80, height=20)

        self.LabelAge = Tkinter.Label(self.root, text='Age:')
        self.LabelAge.place(x=170, y=30, width=80, height=20)
        self.entryAge = Tkinter.Entry(self.root, width=80, textvariable=self.varAge)
        self.entryAge.place(x=270, y=30, width=80, height=20)

        self.LabelUserfeeling = Tkinter.Label(self.root, text='Actual Feel:')
        self.LabelUserfeeling.place(x=10, y=90, width=80, height=20)

        self.entryuser_actual_feeling = Tkinter.Entry(self.root, width=80, textvariable=self.User_enter_feel)
        # self.entryuser_actual_feeling.bind('<Key>', self.printkey)
        self.entryuser_actual_feeling.place(x=100, y=90, width=80, height=20)

        self.CurrentTrial = StringVar()
        self.TrialInfo = StringVar()

        self.show_info = ""  # Information showed on the panel
        self.write_info = ""  # Information written to the records file

        self.user_name = ""
        self.user_age = ""
        self.user_gender = ""

        Info = Label(self.root, textvariable=self.TrialInfo)
        Info.place(x=350, y=0, width=300, height=150)

        Next_Personal = Tkinter.Button(self.root, text='Next Person', command=self.NextPersonal)
        Next_Personal.place(x=270, y=90, width=80, height=20)

        img_1 = Image.open('img/F01.jpg')
        img_1 = img_1.resize((100, 150), Image.ANTIALIAS)
        img_1 = ImageTk.PhotoImage(img_1)

        img_2 = Image.open('img/F02.jpg')
        img_2 = img_2.resize((100, 150), Image.ANTIALIAS)
        img_2 = ImageTk.PhotoImage(img_2)

        img_3 = Image.open('img/F03.jpg')
        img_3 = img_3.resize((100, 150), Image.ANTIALIAS)
        img_3 = ImageTk.PhotoImage(img_3)

        img_4 = Image.open('img/F04.jpg')
        img_4 = img_4.resize((100, 150), Image.ANTIALIAS)
        img_4 = ImageTk.PhotoImage(img_4)

        img_5 = Image.open('img/F05.jpg')
        img_5 = img_5.resize((100, 150), Image.ANTIALIAS)
        img_5 = ImageTk.PhotoImage(img_5)

        img_6 = Image.open('img/F06.jpg')
        img_6 = img_6.resize((100, 150), Image.ANTIALIAS)
        img_6 = ImageTk.PhotoImage(img_6)

        img_7 = Image.open('img/F07.jpg')
        img_7 = img_7.resize((100, 150), Image.ANTIALIAS)
        img_7 = ImageTk.PhotoImage(img_7)

        img_8 = Image.open('img/F08.jpg')
        img_8 = img_8.resize((100, 150), Image.ANTIALIAS)
        img_8 = ImageTk.PhotoImage(img_8)

        # CheckBox for Force Profile
        self.FP1 = Label(self.root, text="Force Profile 1")
        self.FP1.place(x=20, y=120)
        Label(self.root, text="abc", image=img_1).place(x=20, y=140)

        self.FP2 = Label(self.root, text="Force Profile 2")
        self.FP2.place(x=170, y=120)
        Label(self.root, text="abc", image=img_2).place(x=170, y=140)

        self.FP3 = Label(self.root, text="Force Profile 3")
        self.FP3.place(x=320, y=120)
        Label(self.root, text="abc", image=img_3).place(x=320, y=140)

        self.FP4 = Label(self.root, text="Force Profile 4")
        self.FP4.place(x=470, y=120)
        Label(self.root, text="abc", image=img_4).place(x=470, y=140)

        self.FP5 = Label(self.root, text="Force Profile 5")
        self.FP5.place(x=20, y=300)
        Label(self.root, text="abc", image=img_5).place(x=20, y=320)

        self.FP6 = Label(self.root, text="Force Profile 6")
        self.FP6.place(x=170, y=300)
        Label(self.root, text="abc", image=img_6).place(x=170, y=320)

        self.FP7 = Label(self.root, text="Force Profile 7")
        self.FP7.place(x=320, y=300)
        Label(self.root, text="abc", image=img_7).place(x=320, y=320)

        self.FP8 = Label(self.root, text="Force Profile 8")
        self.FP8.place(x=470, y=300)
        Label(self.root, text="abc", image=img_8).place(x=470, y=320)

        self.buttonOk = Tkinter.Button(self.root, text='Confirm', command=self.login)
        self.buttonOk.place(x=20, y=60, width=60, height=20)
        self.buttonCancel = Tkinter.Button(self.root, text='Cancel', command=self.cancel)
        self.buttonCancel.place(x=150, y=60, width=60, height=20)

        self.outputfile = None

        self.root.mainloop()

    # Enter the user's information before trial
    def login(self):
        user_num = self.entryNum.get()

        if user_num == "":
            tkMessageBox.showinfo(title='Warning', message='Please complete number')
            return

        if user_num.isdigit() and 0 < int(user_num) < 17:

            self.user_name = self.entryName.get()
            self.user_age = self.entryAge.get()
            self.user_gender = self.entryGender.get()

            if self.user_name == "":
                tkMessageBox.showinfo(title='Warning', message='Please complete name')
                return

            if self.user_age == "":
                tkMessageBox.showinfo(title='Warning', message='Please complete age')
                return

            if self.user_gender == "":
                tkMessageBox.showinfo(title='Warning', message='Please complete gender')
                return

            self.cmd.start_up(int(user_num))     # Produce commands by user number
            self.cmd.read_command()              # Read commands => commands
            tkMessageBox.showinfo(title='Info', message='Welcome, Begin Trials')

            self.entryNum.config(state="disabled")
            self.entryName.config(state="disabled")
            self.entryAge.config(state="disabled")
            self.entryGender.config(state="disabled")

            # write the head information to the first 4 line in the file
            self.outputfile = open("Records/User_"+str(user_num)+"_record.txt", "w")
            self.outputfile.write("User_name, User_age, User_gender, Times, Recognition Load, Handness, Force Profile, Repeated Times, User Choice, Duration Time \n")
            self.outputfile.close()
            # Re-open the output file again for later record useage
            self.outputfile = open("Records/User_"+str(user_num)+"_record.txt", "a")
        else:
            tkMessageBox.showinfo('Please enter an valid number[0-16]', message='Error')

    def cancel(self):
        self.varNum.set('')

    def center_window(self, root, width, height):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
        # print(size)
        root.geometry(size)

    def NextPersonal(self):
        self.entryNum.config(state="normal")
        self.entryName.config(state="normal")
        self.entryAge.config(state="normal")
        self.entryGender.config(state="normal")

    def change(self):
        if self.User_feel_FP != -1:
            tkMessageBox.showinfo(title='Info', message='User_feel_FP' + str(self.User_feel_FP))

    def printkey(self, event):
        print('You Entered: ' + event.char)
        # if event.char.:
        #     self.User_feel_FP = int(event.char)

    def EnterPress(self, event=None):
        if self.entryuser_actual_feeling.get() == "":
            tkMessageBox.showinfo('Warning', message='Please enter your actual feel before proceed')
        else:
            self.User_feel_FP = int(self.entryuser_actual_feeling.get())

            if self.User_feel_FP == -1:
                tkMessageBox.showinfo(title='Notice', message='Please have a choice')
                return

            self.write_info += str(self.User_feel_FP) + "\n"
            self.outputfile.write(self.write_info)
            tkMessageBox.showinfo(title='Notice', message='Successfully Entered')
            self.entryuser_actual_feeling.delete(0, 'end')

            self.show_info = ""
            self.write_info = ""
            self.User_feel_FP = -1

    def SpaceContinue(self, event):
        if event.keysym == "space":
            print "Space Entered"

            if self.global_times_counter % 2 == 0:
                self.start = int(round(time.time() * 1000))

                # tkMessageBox.showinfo(title='Notice', message='Let\'s begin the trial')
                currentTrial = self.cmd.read_command_by_line()
                print currentTrial

                # Current/Total times
                self.write_info += self.user_name +","+ self.user_age +"," +self.user_gender+","

                current_time = (self.global_times_counter + 1)/2 + 1
                self.show_info += "Total Times: " + str(current_time) + "/288 \n"
                self.write_info += str(current_time) + ","
                currFP = ""
                for i in range(len(currentTrial)):
                    if i == 0:
                        if currentTrial[i] == 1:
                            self.show_info += "Recognition Load: True\n"
                            self.write_info += "1,"
                        else:
                            self.show_info += "Recognition Load: False\n"
                            self.write_info += "0,"
                    if i == 1:
                        if currentTrial[i] == 1:
                            self.show_info += "Handness: True\n"
                            self.write_info += "1,"
                        else:
                            self.show_info += "Handness: False\n"
                            self.write_info += "0,"
                    if i == 2:
                        self.show_info += "Force_Profile: " + currentTrial[i] + "\n"
                        self.write_info += currentTrial[i] + ","
                        currFP = currentTrial[i]
                    if i == 3:
                        self.show_info += "Repeated_Times: " + currentTrial[i] + "\n"
                        self.write_info += currentTrial[i] + ","

                self.TrialInfo.set(self.show_info)
                self.global_times_counter += 1

                self.spring = Spring()
                self.spring.set_profile(currFP)
                self.spring.run()

            else:  # self.global_times_counter % 2 == 1 Stop the current trial
                self.spring.terminate()
                self.end = int(round(time.time() * 1000))
                self.deltatime = self.end - self.start
                # Write the timestamp
                self.write_info += str(self.deltatime)+","
                self.entryuser_actual_feeling.delete(0, 'end')
                self.global_times_counter += 1

if "__main__":
    Experiment_Session()
