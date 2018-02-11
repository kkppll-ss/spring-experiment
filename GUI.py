# -*- coding: UTF-8 -*-

import Tkinter
import tkMessageBox
import Produce_Read_Order_List
from Tkinter import *
import ImageTk
import Image
import datetime
import time


class Experiment_Session:

    def __init__(self):
        root = Tkinter.Tk()
        root.title("Haptic Experiment")
        self.center_window(root, 600, 600)
        root.maxsize(800, 600)
        root.minsize(300, 240)
        self.cmd = Produce_Read_Order_List.Produce_Read_Order_List()
        self. cmd.make_pairs()
        self.User_feel_FP = -1               # record the user's actual choice of haptic feeling
        self.global_times_counter = 0        # record the user's repeated times
        self.FP_status_0 = IntVar()
        self.FP_status_1 = IntVar()
        self.FP_status_2 = IntVar()
        self.FP_status_3 = IntVar()
        self.FP_status_4 = IntVar()
        self.FP_status_5 = IntVar()
        self.FP_status_6 = IntVar()
        self.FP_status_7 = IntVar()

        self.varNum = Tkinter.StringVar(value='')
        self.varName = Tkinter.StringVar(value='')
        self.varGender = Tkinter.StringVar(value='')
        self.varAge = Tkinter.StringVar(value='')

        self.labelNum = Tkinter.Label(root, text='User Num:')
        self.labelNum.place(x=10, y=5, width=80, height=20)
        self.entryNum = Tkinter.Entry(root, width=80, textvariable=self.varNum)
        self.entryNum.place(x=100, y=5, width=80, height=20)

        self.LabelName = Tkinter.Label(root, text='Name:')
        self.LabelName.place(x=10, y=30, width=80, height=20)
        self.entryName = Tkinter.Entry(root, width=80, textvariable=self.varName)
        self.entryName.place(x=100, y=30, width=80, height=20)

        self.LabelGender = Tkinter.Label(root, text='Gender:')
        self.LabelGender.place(x=170, y=5, width=80, height=20)
        self.entryGender = Tkinter.Entry(root, width=80, textvariable=self.varGender)
        self.entryGender.place(x=270, y=5, width=80, height=20)

        self.LabelAge = Tkinter.Label(root, text='Age:')
        self.LabelAge.place(x=170, y=30, width=80, height=20)
        self.entryAge = Tkinter.Entry(root, width=80, textvariable=self.varAge)
        self.entryAge.place(x=270, y=30, width=80, height=20)

        self.CurrentTrial = StringVar()
        self.TrialInfo = StringVar()

        Next = Tkinter.Button(root, text='Next Trial', command=self.NextTrial)
        Next.place(x=270, y=60, width=80, height=20)

        Info = Label(root, textvariable=self.TrialInfo)
        Info.place(x=350, y=0, width=300, height=150)

        Next_Personal = Tkinter.Button(root, text='Next Person', command=self.NextPersonal)
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
        self.FP1 = Checkbutton(root, text="Force Profile 1", variable=self.FP_status_0, command=self.change)
        self.FP1.place(x=20, y=120)
        Label(root, text="abc", image=img_1).place(x=20, y=140)

        self.FP2 = Checkbutton(root, text="Force Profile 2", variable=self.FP_status_1, command=self.change)
        self.FP2.place(x=170, y=120)
        Label(root, text="abc", image=img_2).place(x=170, y=140)

        self.FP3 = Checkbutton(root, text="Force Profile 3", variable=self.FP_status_2, command=self.change)
        self.FP3.place(x=320, y=120)
        Label(root, text="abc", image=img_3).place(x=320, y=140)

        self.FP4 = Checkbutton(root, text="Force Profile 4", variable=self.FP_status_3, command=self.change)
        self.FP4.place(x=470, y=120)
        Label(root, text="abc", image=img_4).place(x=470, y=140)

        self.FP5 = Checkbutton(root, text="Force Profile 5", variable=self.FP_status_4, command=self.change)
        self.FP5.place(x=20, y=280)
        Label(root, text="abc", image=img_5).place(x=20, y=300)

        self.FP6 = Checkbutton(root, text="Force Profile 6", variable=self.FP_status_5, command=self.change)
        self.FP6.place(x=170, y=280)
        Label(root, text="abc", image=img_6).place(x=170, y=300)

        self.FP7 = Checkbutton(root, text="Force Profile 7", variable=self.FP_status_6, command=self.change)
        self.FP7.place(x=320, y=280)
        Label(root, text="abc", image=img_7).place(x=320, y=300)

        self.FP8 = Checkbutton(root, text="Force Profile 8", variable=self.FP_status_7, command=self.change)
        self.FP8.place(x=470, y=280)
        Label(root, text="abc", image=img_8).place(x=470, y=300)

        self.buttonOk = Tkinter.Button(root, text='Confirm', command=self.login)
        self.buttonOk.place(x=20, y=60, width=60, height=20)
        self.buttonCancel = Tkinter.Button(root, text='Cancel', command=self.cancel)
        self.buttonCancel.place(x=150, y=60, width=60, height=20)

        self.outputfile = None

        root.mainloop()

    # Enter the User Number to begin the first trial
    def login(self):
        user_num = self.entryNum.get()
        if user_num.isdigit() and 0 < int(user_num) < 17:

            self.cmd.start_up(int(user_num))     # Produce commands by user number
            self.cmd.read_command()  # Read commands => commands
            tkMessageBox.showinfo(title='Info', message='Welcome, Begin Trials')

            user_name = self.entryName.get()
            user_age = self.entryAge.get()
            user_gender = self.entryGender.get()

            self.entryNum.config(state="disabled")
            self.entryName.config(state="disabled")
            self.entryAge.config(state="disabled")
            self.entryGender.config(state="disabled")

            # write the head information to the first 4 line in the file
            self.outputfile = open("User_"+str(user_num)+"_record.txt", "w")
            self.outputfile.write("User_name: " + user_name + "\n")
            self.outputfile.write("User_age: " + user_age + "\n")
            self.outputfile.write("User_gender: " + user_gender + "\n")
            self.outputfile.write("Times/Total, Timestamp, Recognition Load, Handness, Force Profile, Repeated Times, User Choice \n")
            self.outputfile.close()
            # Re-open the output file again for later record useage
            self.outputfile = open("User_" + str(user_num)+"_record.txt", "a")
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

    def NextTrial(self):
        if self.global_times_counter == 0:
            tkMessageBox.showinfo(title='Notice', message='Let\'s begin the first trial')
            self.global_times_counter += 1
        else:
            tkMessageBox.showinfo(title='Notice', message='Now proceed to next trial')
            currentTrial = self.cmd.read_command_by_line()
            print currentTrial

            show_info = ""   # Information showed on the panel
            write_info = ""  # Information written to the records file

            # Current/Total times
            show_info += "Total Times: " + str(self.global_times_counter) + "/288 \n"
            write_info += str(self.global_times_counter) + "/288, "

            # Write the timestamp
            write_info += datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+", "

            for i in range(len(currentTrial)):
                if i == 0:
                    if currentTrial[i] == 1:
                        show_info += "Recognition Load: True\n"
                        write_info += "True, "
                    else:
                        show_info += "Recognition Load: False\n"
                        write_info += "False, "
                if i == 1:
                    if currentTrial[i] == 1:
                        show_info += "Handness: True\n"
                        write_info += "True, "
                    else:
                        show_info += "Handness: False\n"
                        write_info += "False, "
                if i == 2:
                    show_info += "Force_Profile: " + currentTrial[i]+"\n"
                    write_info += currentTrial[i]+", "
                if i == 3:
                    show_info += "Repeated_Times: " + currentTrial[i]+"\n"
                    write_info += currentTrial[i] + ", "

            # if self.User_feel_FP == -1:
                
            write_info += str(self.User_feel_FP) + "\n"
            # self.outputfile = open("User" + str(int(self.entryNum.get()) - 1) + ".txt", "a")
            self.outputfile.write(write_info)
            self.TrialInfo.set(show_info)
            self.FP_status_0.set(0)
            self.FP_status_1.set(0)
            self.FP_status_2.set(0)
            self.FP_status_3.set(0)
            self.FP_status_4.set(0)
            self.FP_status_5.set(0)
            self.FP_status_6.set(0)
            self.FP_status_7.set(0)

            self.global_times_counter += 1
            # print str(global_times_counter) + "/288"

    def change(self):

        if self.FP_status_0.get() == 1:   # if clicked
            self.User_feel_FP = 0
        # elif FP_status_0.get() == 0:
        #     User_feel_FP = -1

        if self.FP_status_1.get() == 1:
            self.User_feel_FP = 1
        # elif FP_status_1.get() == 0 and User_feel_FP == -1:
        #     User_feel_FP = -1

        if self.FP_status_2.get() == 1:
            self.User_feel_FP = 2
        # elif FP_status_1.get() == 0:
        #     User_feel_FP = -1

        if self.FP_status_3.get() == 1:
            self.User_feel_FP = 3
        # elif FP_status_3.get() == 0:
        #     User_feel_FP = 3

        if self.FP_status_4.get() == 1:
            self.User_feel_FP = 4

        if self.FP_status_5.get() == 1:
            self.User_feel_FP = 5
        # elif FP_status_5.get() == 0:
        #     User_feel_FP = 5

        if self.FP_status_6.get() == 1:
            self.User_feel_FP = 6
        # elif FP_status_6.get() == 0:
        #     User_feel_FP = 6

        if self.FP_status_7.get() == 1:
            self.User_feel_FP = 7
        # elif FP_status_7.get() == 0:
        #     User_feel_FP = 7

        if self.User_feel_FP != -1:
            tkMessageBox.showinfo(title='Info', message='User_feel_FP' + str(self.User_feel_FP+1))


Experiment_Session()
