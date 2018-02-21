# -*- coding: UTF-8 -*-

import time
import datetime
import Tkinter
import tkMessageBox
import Produce_Read_Order_list as Produce_Read_Order_List
from Play_electronic_element import play_electronic_element
from Recover_from_Record import *
from Tkinter import *
import ImageTk
import Image
import random
from spring import Spring


class Experiment_Session:

    def __init__(self):
        # Set the basic params of windows
        self.root = Tkinter.Tk()
        self.root.title("Haptic Experiment")
        w = 1920
        h = 1080
        self.width = w
        self.height = h
        self.root.geometry("%dx%d" % (w, h))
        self.root.minsize(300, 240)

        self.user_num = -1
        self.user_name = ""
        self.user_gender = ""
        self.user_age = 0
        self.haptic_feel_lookup = {
            1: 'empty',
            2: 'low',
            3: 'high',
            4: 'medium',
            5: 'click',
            6: 'drop',
            7: 'None'
        }

        self.cmd = Produce_Read_Order_List.Produce_Read_Order_List()  # Initiate list of command

        self.User_feel_FP = ""              # record the user's actual choice of haptic feeling
        self.global_times_counter = 0       # record the user's repeated times
        self.current_time = 0
        self.correct_times = 0
        self.correct_RL_times = 0
        self.RL_total = 0
        self.start = 0                      # Start timestamp for haptic sensing
        self.end = 0                        # End timestamp for haptic sensing
        self.deltatime = 0                  # The time duration for haptic sensing
        self.startTrialNum = 0              # Start number specified for program crash
        self.outputfile = None              # Output file for trial recording
        self.currentTrial = None            # Current trial information
        self.play_electronic_element = None # Define the instance of electronic element sound play
        self.SpacePressTime = 0             # Times of press [Space]
        self.EnterPressTime = 0             # Times of press [Enter]
        self.PressSpaceTwice = False        # Space pressed for more than twice without [Enter]
        self.user_choice = -1               # User choice of last i'th electronic element
        self.ask_last_num = -1              # the last i'th elements hear of under the Recongnition load
        self.write_info = ""                # Information written to output file
        self.show_info = ""                 # Information showed on the panel
        self.pin_height = ""                # Information of the pin height
        self.last_num = []                  # list for last ask number contains [2(27), 1(27)]

        self.space_sound_start = ""          # Timestamp of Space and music start time
        self.force_profile_start = ""        # Timestamp of Force profile start
        self.sound_stop = ""                 # Timestamp of sound stop
        self.space_curTrial_stop = ""         # Timestamp of current trial stop

        # Switch between show debug and not show
        self.show_debug = False

        self.TrialInfo = Tkinter.StringVar(value='')                # Trial information
        self.Answer = Tkinter.StringVar(value='')                   # User answer
        self.Question_text = Tkinter.StringVar(value='')            # Text of Question
        self.Position_Info = Tkinter.StringVar(value='')            # Position Information about the Spring
        self.Debug_Info = Tkinter.StringVar(value='')               # Debug Information about the Spring

        # Bind the Space Key press to continue
        self.root.bind("<KeyPress>", self.SpaceContinue)            # Bind the [Space] press and its function
        self.root.focus_set()
        self.root.bind('<Return>', self.EnterPress)                  # Bind the [Enter] Key press
        # self.spring = Spring()

        self.varNum = Tkinter.StringVar(value='')
        self.varName = Tkinter.StringVar(value='')
        self.varGender = Tkinter.StringVar(value='')
        self.varAge = Tkinter.StringVar(value='')

        # Top level Panel for user information enter, show at program boot, hide when information entered and confirmed
        top_entry_y = h/80
        top_col_1 = w/15
        top_col_2 = top_col_1 + w/12 + w/18
        top_col_3 = top_col_2 + w/12 + w/18
        top_col_4 = top_col_3 + w/12 + w/18
        top_col_5 = top_col_4 + w / 12 + w / 15
        top_col_6 = top_col_5 + w / 12 + w / 12

        self.labelNum = Tkinter.Label(self.root, text='User Num:')
        self.labelNum.place(x=top_col_1, y=top_entry_y, width=w/12, height=h/20)
        self.labelNum.config(font=("Courier", 15, "bold"))
        self.entryNum = Tkinter.Entry(self.root, textvariable=self.varNum)
        self.entryNum.place(x=top_col_1 + w/12, y=top_entry_y, width=w/18, height=h/20)

        self.LabelName = Tkinter.Label(self.root, text='Name:')
        self.LabelName.place(x=top_col_2, y=top_entry_y, width=w/12, height=h/20)
        self.LabelName.config(font=("Courier", 15, "bold"))
        self.entryName = Tkinter.Entry(self.root, textvariable=self.varName)
        self.entryName.place(x=top_col_2 + w/12, y=top_entry_y, width=w/20, height=h/20)

        self.LabelGender = Tkinter.Label(self.root, text='Gender:')
        self.LabelGender.place(x=top_col_3, y=top_entry_y, width=w/12, height=h/20)
        self.LabelGender.config(font=("Courier", 15, "bold"))
        self.entryGender = Tkinter.Entry(self.root, width=80, textvariable=self.varGender)
        self.entryGender.place(x=top_col_3 + w/12, y=top_entry_y, width=w/20, height=h/20)

        self.LabelAge = Tkinter.Label(self.root, text='Age:')
        self.LabelAge.place(x=top_col_4, y=top_entry_y, width=w/12, height=h/20)
        self.LabelAge.config(font=("Courier", 15, "bold"))
        self.entryAge = Tkinter.Entry(self.root, width=80, textvariable=self.varAge)
        self.entryAge.place(x=top_col_4 + w/12, y=top_entry_y, width=w/20, height=h/20)

        self.LabelStartFromTrial = Tkinter.Label(self.root, text='Start Num:')
        self.LabelStartFromTrial.place(x=top_col_5, y=top_entry_y, width=w / 12, height=h / 20)
        self.LabelStartFromTrial.config(font=("Courier", 15, "bold"))
        self.entryStartFromTrial = Tkinter.Entry(self.root, width=80, textvariable=self.startTrialNum)
        self.entryStartFromTrial.place(x=top_col_5 + w/12, y=top_entry_y, width=w / 20, height=h / 20)

        self.buttonOk = Tkinter.Button(self.root, text='Confirm', command=self.login)
        self.buttonOk.place(x=top_col_6, y=top_entry_y, width=w / 20, height=h / 20)
        self.buttonOk.config(font=("Courier", 12, "bold"))
        self.buttonCancel = Tkinter.Button(self.root, text='Cancel', command=self.cancel)
        self.buttonCancel.place(x=top_col_6 + w/18, y=top_entry_y, width=w / 20, height=h / 20)
        self.buttonCancel.config(font=("Courier", 12, "bold"))

        self.buttonRetry = Tkinter.Button(self.root, text='Retry', command=self.retry)
        self.buttonRetry.place(x=top_col_6 + 2 * w/18, y=top_entry_y, width=w / 20, height=h / 20)
        self.buttonRetry.config(font=("Courier", 12, "bold"))

        self.Info_Header = Label(self.root, text="Trial\tRecongition Load\tComponent", anchor=W)
        self.Info_Header.config(font=("Courier", 12, "bold"))

        self.Info = Label(self.root, textvariable=self.TrialInfo, anchor=W)
        self.Info.config(font=("Courier", 12, "bold"))

        img_dx = w/5
        img_dy = h/5

        # Set up and place the images at the second level
        img_1 = Image.open('img/F01.jpg')
        img_1 = img_1.resize((img_dx, img_dy), Image.ANTIALIAS)
        img_1 = ImageTk.PhotoImage(img_1)

        img_2 = Image.open('img/F02.jpg')
        img_2 = img_2.resize((img_dx, img_dy), Image.ANTIALIAS)
        img_2 = ImageTk.PhotoImage(img_2)

        img_3 = Image.open('img/F03.jpg')
        img_3 = img_3.resize((img_dx, img_dy), Image.ANTIALIAS)
        img_3 = ImageTk.PhotoImage(img_3)

        img_4 = Image.open('img/F04.jpg')
        img_4 = img_4.resize((img_dx, img_dy), Image.ANTIALIAS)
        img_4 = ImageTk.PhotoImage(img_4)

        img_5 = Image.open('img/F05.jpg')
        img_5 = img_5.resize((img_dx, img_dy), Image.ANTIALIAS)
        img_5 = ImageTk.PhotoImage(img_5)

        img_6 = Image.open('img/F06.jpg')
        img_6 = img_6.resize((img_dx, img_dy), Image.ANTIALIAS)
        img_6 = ImageTk.PhotoImage(img_6)

        col_x_1 = 2 * w / 20
        col_x_2 = 4 * w/20 + img_dx
        col_x_3 = 6 * w/20 + 2 * img_dx

        label_level_1_y = top_entry_y + 2 * h/20
        label_level_2_y = top_entry_y + 4 * h / 20 + img_dy

        img_level_1_y = top_entry_y + 3 * h/20
        img_level_2_y = top_entry_y + 5 * h / 20 + img_dy

        self.FP1 = Label(self.root, text="1. empty", fg='blue')
        self.FP1.place(x=col_x_1, y=label_level_1_y)
        self.FP1.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_1).place(x=col_x_1, y=img_level_1_y)

        self.FP2 = Label(self.root, text="2. low", fg='blue')
        self.FP2.place(x=col_x_2, y=label_level_1_y)
        self.FP2.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_2).place(x=col_x_2, y=img_level_1_y)

        self.FP3 = Label(self.root, text="3. high", fg='blue')
        self.FP3.place(x=col_x_3, y=label_level_1_y)
        self.FP3.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_3).place(x=col_x_3, y=img_level_1_y)

        self.FP4 = Label(self.root, text="4. medium", fg='blue')
        self.FP4.place(x=col_x_1, y=label_level_2_y)
        self.FP4.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_4).place(x=col_x_1, y=img_level_2_y)

        self.FP5 = Label(self.root, text="5. click", fg='blue')
        self.FP5.place(x=col_x_2, y=label_level_2_y)
        self.FP5.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_5).place(x=col_x_2, y=img_level_2_y)

        self.FP6 = Label(self.root, text="6. drop", fg='blue')
        self.FP6.place(x=col_x_3, y=label_level_2_y)
        self.FP6.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_6).place(x=col_x_3, y=img_level_2_y)

        # User haptic feel part and Quize part
        self.Question = Label(self.root, textvariable=self.Question_text)

        # Show the current position information on right side
        self.CurrPosition = Label(self.root, text="Position Info", textvariable=self.Position_Info)
        self.CurrPosition.place(x=12 * self.width / 16, y=7 * self.height / 8)
        self.CurrPosition.config(font=("Courier", 15, "bold"), fg="red")

        # Show the Force Profile on left side
        self.CurrDebug = Label(self.root, text="Debug Info", textvariable=self.Debug_Info)
        if self.show_debug:
            self.CurrDebug.place(x=2 * self.width / 16, y=3 * self.height / 4)
            self.CurrDebug.config(font=("Courier", 20, "bold"), fg="red")

        self.User_Answer = Tkinter.Label(self.root, text='Answer: ', fg="blue")
        self.User_Answer.place(x=w/2 - w/8, y=7*h/8)
        self.User_Answer.config(font=("Courier", 20, "bold"))
        self.entry_Answer = Tkinter.Entry(self.root, width=80, textvariable=self.Answer)
        self.entry_Answer.place(x=w/2 - w/25, y=7*h/8, width=w / 12, height=h / 25)

        self.read_first_100 = []

        f_first = open("First_100.txt", 'r')

        self.word_pron = []
        for i in f_first:
            self.word_pron.append(i)
        self.produce_random_list()

        self.root.mainloop()

    def login(self):

        if self.entryNum.get() == "":
            tkMessageBox.showinfo(title='Warning', message='Please complete number')
            return

        self.user_num = int(self.entryNum.get())

        if 0 < self.user_num < 13:

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
            if self.entryStartFromTrial.get() != "":
                self.startTrialNum = int(self.entryStartFromTrial.get())

            # check the existence of program crash
            if self.startTrialNum != 0:
                existFilename = "Order_List/User_" + str(self.user_num) + "_order_list.txt"
                self.cmd.read_command(existFilename)            # Read commands => commands in existence file
                self.correct_RL_times, self.RL_total = Recover_from_Record("Records/User_" + str(self.user_num) + "_record.txt")
            else:
                self.cmd.start_up(int(self.user_num))  # Produce commands by user number
                self.cmd.read_command()           # Read commands => commands
                # write the head information to the first line in the file
                self.outputfile = open("Records/User_" + str(self.user_num) + "_record.txt", "w")
                self.outputfile.write("User_num,User_name,User_age,User_gender,Trials,Pin_height,Recognition_Load,Force_Profile,Component_Num,Duration_Time,User_Choice,Haptic_Choice_Correctness, ask_last_num,Recognition_Load_Correctness,space_sound_start,force_profile_start,sound_stop,space_curTrial_stop\n")
                self.outputfile.close()

            # Re-open the output file again for later record useage
            self.outputfile = open("Records/User_" + str(self.user_num) + "_record.txt", "a")
        else:
            tkMessageBox.showinfo('Error', message='Please enter an valid number[0-12]')
            return

        # Hide the label and entry from the panel
        self.labelNum.place_forget()
        self.entryNum.place_forget()
        self.LabelName.place_forget()
        self.entryName.place_forget()
        self.LabelGender.place_forget()
        self.entryGender.place_forget()
        self.LabelAge.place_forget()
        self.entryAge.place_forget()
        self.LabelStartFromTrial.place_forget()
        self.entryStartFromTrial.place_forget()
        self.buttonOk.place_forget()
        self.buttonCancel.place_forget()

        # Show the trial information after confirmation
        self.Info_Header.place(x=30 * self.width / 80, y= self.height / 80, width=17 * self.width / 64, height=self.height / 25)
        self.Info_Header.config(bg="red", fg="white")
        self.Info_Header.config(font=("Courier", 15, "bold"))

        self.Info.place(x=30 * self.width/80, y=self.height/80 + self.height/22, width=17 * self.width /64, height=self.height/25)
        self.Info.config(font=("Courier", 15, "bold"))
        self.Info.config(bg="blue", fg="white")

    def cancel(self):
        self.varNum.set('')
        self.varAge.set('')
        self.varGender.set('')
        self.varName.set('')

    # Start and End a haptic trial by [Space] keypress
    def SpaceContinue(self, event):

        if event.keysym == "space":
            # Press [Enter] for 1,3,5,7,9
            if self.EnterPressTime == 0:
                tkMessageBox.showinfo('Warning', message='Press [Enter] to start a trial before proceed')
                return

            # Press Space more than twice without press [Enter]
            if self.PressSpaceTwice is True:
                tkMessageBox.showinfo('Warning', message='Answer the question before proceed')
                return

            print "Space Entered"
            if self.SpacePressTime % 2 == 0:
                self.Question_text.set("Sound START")
                self.Question.place(x=7 * self.width / 16, y=3 * self.height / 4)
                self.Question.config(fg="red", font=("Courier", 23, "bold"))
                # Start to play sounds in recognition load
                if self.currentTrial[1] == '1':
                    self.play_electronic_element = play_electronic_element()
                    self.play_electronic_element.start()
                    self.space_sound_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()[1]
                else:
                    self.space_sound_start = "-1"
            else:
                # Stop the movement of Haptic Spring
                self.spring.terminate()
                self.deltatime = int(round(time.time() * 1000)) - self.start
                self.Question_text.set("Haptic Test END, Select a Haptic Feel")
                self.space_curTrial_stop = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()[1]
                self.PressSpaceTwice = True
            self.SpacePressTime += 1

    # [Enter] Press for 1. Show a Trial Information 2. Show a electronic elements
    def EnterPress(self, event):

        # Incomplete Personal Information
        if self.EnterPressTime == 0:
            if self.user_num == -1 or self.user_name == "" or self.user_gender == "" or self.user_age == "":
                tkMessageBox.showinfo('Warning', message='Complete Personal Info before proceed')
                return

        # the first time press [Enter]: show a Trial Information
        if self.EnterPressTime == 0:

            start_num = self.startTrialNum
            if start_num == 0:
                self.currentTrial = self.cmd.read_command_by_line()
            while start_num != 0:
                self.currentTrial = self.cmd.read_command_by_line()
                start_num -= 1

            print self.currentTrial

            # Current/Total times
            self.write_info += str(self.user_num)+","+self.user_name+","+str(self.user_age)+","+self.user_gender+","

            if self.startTrialNum == 0:
                self.current_time = self.global_times_counter + 1
            else:
                self.current_time = self.global_times_counter + self.startTrialNum

            self.show_info += "  "+str(self.current_time) + "\t   "
            self.write_info += str(self.current_time) + ","

            for i in range(len(self.currentTrial)):
                if i == 0:
                    self.pin_height = self.currentTrial[i]
                    self.write_info += str(self.cmd.condition_lookup_table.index(self.pin_height))+","
                if i == 1:
                    if self.currentTrial[i] == '1':
                        self.show_info += "  True\t\t"
                        self.write_info += "1,"
                    else:
                        self.show_info += "  False\t\t"
                        self.write_info += "0,"
                if i == 2:
                    self.write_info += str(self.cmd.Force_Profile.index(self.currentTrial[i])) + ","
                    self.Debug_Info.set("FP: " + self.currentTrial[i])
                if i == 3:
                    self.show_info += self.cmd.Electronic_Element_Component_lookup[self.currentTrial[i]]
                    self.write_info += self.currentTrial[i] + ","

            self.TrialInfo.set(self.show_info)
            self.global_times_counter += 1
            self.show_info = ""
            self.spring_start()

        elif self.EnterPressTime % 2 == 1:

            # Incomplete Haptic Test Start--End
            if self.PressSpaceTwice is False:
                tkMessageBox.showinfo('Warning', message='Finish Haptic Test before proceed Press [Space]')
                return

            if len(self.entry_Answer.get()) == 0:
                tkMessageBox.showinfo('Warning', message='Enter your haptic feel before proceed')
                return
            else:
                if self.entry_Answer.get().strip().isdigit() and 0 < int(self.entry_Answer.get().strip()) < 8:
                    self.User_feel_FP = self.haptic_feel_lookup[int(self.entry_Answer.get())]
                    result = tkMessageBox.askyesno(title='Notice', message='Your Haptic Choice: ' + self.User_feel_FP +'\nCan you confirm ?')
                    if result is True:
                        pass
                    else:
                        return
                else:
                    tkMessageBox.showinfo(title='Warning', message='Your Choice MUST BE Integer in [1-7]')
                    return

                self.Answer.set("")

                # Show the recognition load question
                if self.currentTrial[1] == '1':
                    self.ask_last_num = self.get_ask_last_num()
                    self.Question_text.set("Select the Last " + str(self.ask_last_num) + " Chinese word\n")
                    print "word_Pronounce: " + self.word_pron[self.play_electronic_element.last_i_th(self.ask_last_num)].decode("gbk")
                else:
                    self.ask_last_num = -1
                    self.Question_text.set("No Question just Press [Enter] to Proceed")

        # Write the current user trial data information to output file
        # and choice and show a trial Information
        elif self.EnterPressTime % 2 == 0:
            # Recognition Load question answer
            if self.currentTrial[1] == '1':
                if len(self.entry_Answer.get()) == 0:
                    tkMessageBox.showinfo('Warning', message='Enter the correctness of recognition Load before proceed')
                    return
                else:
                    if self.entry_Answer.get().strip().isdigit():
                        self.user_choice = int(self.entry_Answer.get())
                    else:
                        tkMessageBox.showinfo(title='Notice', message='Your Choice MUST BE Integer in [1-9]')
                        return

                result = tkMessageBox.askyesno('Notice', message='Your Recognition Load Correctness: ' + str(self.user_choice) + '\nCan you confirm ?')
                if result is True:
                    pass
                else:
                    return
            else:
                self.user_choice = -1

            self.Question_text.set("")
            self.Answer.set("")

            self.write_info += str(self.deltatime) + ","

            if self.User_feel_FP != 'None':
                self.write_info += str(self.cmd.Force_Profile.index(self.User_feel_FP)) + ","
                if self.User_feel_FP == self.currentTrial[2]:
                    self.write_info += str(1) + ","
                    self.correct_times += 1
                else:
                    self.write_info += str(0) + ","
            else:
                self.write_info += str(7) + ','

            print "Actual FP: " + self.currentTrial[2] + "----User FP: " + self.User_feel_FP
            print "***" + str(self.correct_times) + "/" + str(self.global_times_counter)

            self.write_info += str(self.ask_last_num) + ","
            if self.currentTrial[1] == '1':
                self.write_info += str(self.user_choice) + ","
                if self.user_choice == 1:
                    self.correct_RL_times += 1
                self.RL_total += 1
            else:
                self.write_info += str(-1) + ","
                self.write_info += str(self.user_choice)
            self.write_info += self.space_sound_start + ","
            self.write_info += self.force_profile_start + ","
            self.write_info += self.sound_stop + ","
            self.write_info += self.space_curTrial_stop + "\n"
            self.outputfile.write(self.write_info)
            self.outputfile.flush()
            self.write_info = ""

            # When the trial times reach the end
            if self.current_time == len(self.cmd.Commands):
                tkMessageBox.showinfo('Notice', message='Haptic Test End, Thank you!!')
                return

            # Begin the next trial
            self.currentTrial = self.cmd.read_command_by_line()
            print self.currentTrial

            # Current/Total times
            self.write_info += str(self.user_num)+","+self.user_name+","+str(self.user_age)+","+self.user_gender+","

            if self.startTrialNum == 0:
                self.current_time = self.global_times_counter + 1
            else:
                self.current_time = self.global_times_counter + self.startTrialNum

            self.show_info += str(self.current_time) + "\t\t"
            self.write_info += str(self.current_time) + ","

            for i in range(len(self.currentTrial)):
                if i == 0:
                    self.pin_height = self.currentTrial[i]
                    self.write_info += str(self.cmd.condition_lookup_table.index(self.pin_height)) + ","
                if i == 1:
                    if self.currentTrial[i] == '1':
                        self.show_info += "True\t\t"
                        self.write_info += "1,"
                    else:
                        self.show_info += "False\t\t"
                        self.write_info += "0,"
                if i == 2:
                    # self.show_info += self.currentTrial[i] + "\t\t"
                    self.Debug_Info.set("FP: " + self.currentTrial[i])
                    self.write_info += str(self.cmd.Force_Profile.index(self.currentTrial[i])) + ","
                if i == 3:
                    self.show_info += self.cmd.Electronic_Element_Component_lookup[self.currentTrial[i]]
                    self.write_info += self.currentTrial[i] + ","

            self.PressSpaceTwice = False
            self.TrialInfo.set(self.show_info)
            if self.RL_total != 0:
                precision = float(self.correct_RL_times)/self.RL_total
                self.Position_Info.set(str(self.correct_RL_times) + "/" + str(self.RL_total) + "=" +str(round(precision * 100)) + "%")
            self.global_times_counter += 1
            self.show_info = ""
            self.spring_start()
            
        self.EnterPressTime += 1

    def retry(self):
        # Recognition Load question answer
        if self.currentTrial[1] == '1':
            if len(self.entry_Answer.get()) == 0:
                tkMessageBox.showinfo('Warning', message='Select the Electronic Element before retry')
                return
            else:
                if self.entry_Answer.get().strip().isdigit() and 0 < int(self.entry_Answer.get().strip()) < 10:
                    self.user_choice = int(self.entry_Answer.get())
                else:
                    tkMessageBox.showinfo(title='Notice', message='Your Choice MUST BE Integer in [1-9]')
                    return
            result = tkMessageBox.askyesno('Notice', message='Your Recognition Load Choice: ' + str(
                self.user_choice) + '\nCan you confirm ?')
            if result is True:
                pass
            else:
                return
        else:
            self.user_choice = -1

        self.Question_text.set("")
        self.Answer.set("")

        self.write_info += str(self.deltatime) + ","

        if self.User_feel_FP != 'None':
            self.write_info += str(self.cmd.Force_Profile.index(self.User_feel_FP)) + ","
            if self.User_feel_FP == self.currentTrial[2]:
                self.write_info += str(1) + ","
                self.correct_times += 1
                print str(self.correct_times) + "/" + str(self.global_times_counter)
            else:
                self.write_info += str(0) + ","
        else:
            self.write_info += str(7) + ','

        self.write_info += str(self.ask_last_num) + ","
        if self.currentTrial[1] == '1':
            self.write_info += str(self.play_electronic_element.last_i_th(self.ask_last_num)) + ","
            self.write_info += str(self.user_choice) + ","
        else:
            self.write_info += str(-1) + ","
            self.write_info += str(self.user_choice) + ","

        self.write_info += self.space_sound_start + ","
        self.write_info += self.force_profile_start + ","
        self.write_info += self.sound_stop + ","
        self.write_info += self.space_curTrial_stop + "\n"
        self.outputfile.write(self.write_info)
        self.outputfile.flush()
        self.write_info = ""

        # Begin the next trial
        print self.currentTrial
        self.global_times_counter -= 1

        # Current/Total times
        self.write_info += str(self.user_num) + "," + self.user_name + "," + str(self.user_age) + "," + self.user_gender + ","

        if self.startTrialNum == 0:
            self.current_time = self.global_times_counter + 1
        else:
            self.current_time = self.global_times_counter + self.startTrialNum

        self.show_info += str(self.current_time) + "\t\t"
        self.write_info += str(self.current_time) + ","

        for i in range(len(self.currentTrial)):
            if i == 0:
                self.pin_height = self.currentTrial[i]
                self.write_info += str(self.cmd.condition_lookup_table.index(self.pin_height)) + ","
            if i == 1:
                if self.currentTrial[i] == '1':
                    self.show_info += "True\t\t"
                    self.write_info += "1,"
                else:
                    self.show_info += "False\t\t"
                    self.write_info += "0,"
            if i == 2:
                self.Debug_Info.set("FP: " + self.currentTrial[i])
                self.write_info += str(self.cmd.Force_Profile.index(self.currentTrial[i])) + ","
            if i == 3:
                self.show_info += self.cmd.Electronic_Element_Component_lookup[self.currentTrial[i]]
                self.write_info += self.currentTrial[i] + ","

        self.PressSpaceTwice = False
        self.TrialInfo.set(self.show_info)
        self.Position_Info.set(str(self.correct_RL_times) + "/" + str(self.RL_total)+ "=" +str(self.correct_RL_times/self.RL_total*1.0))
        self.show_info = ""
        self.global_times_counter += 1
        self.EnterPressTime += 1

        self.spring_start()

    def spring_start(self):
        self.spring = Spring(self.time_counter, self.sound_stopper)
        Pin_height = int(self.currentTrial[3])
        if 1 <= Pin_height and Pin_height <=3:
            self.spring.set_profile(self.currentTrial[2], 'long')
        elif 4 <= Pin_height and Pin_height <=6:
            self.spring.set_profile(self.currentTrial[2], 'middle')
        elif 7 <= Pin_height and Pin_height <= 9:
            self.spring.set_profile(self.currentTrial[2], 'short')
        self.spring.start()

    # must be called at __init__
    def produce_random_list(self):

        for i in range(54):
            self.last_num.append(1)

        for i in range(27):
            index = random.randrange(0, 54)
            while self.last_num[index] != 1:
                index = random.randrange(0, 54)
                pass
            self.last_num[index] = 2

    # Each time when recognition load ask question
    def get_ask_last_num(self):
        return self.last_num.pop()

    def time_counter(self):

        if self.SpacePressTime%2 != 1:
            tkMessageBox.showinfo('Warning', message='Press [Space] before Force Profile Sense')
            return

        self.start = int(round(time.time() * 1000))
        self.Question_text.set("Haptic Test START")
        self.force_profile_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()[1]
        self.Question.place(x=6 * self.width / 16, y=3 * self.height / 4)
        self.Question.config(font=("Courier", 23, "bold"))
        self.Question.config(fg="green")

    def sound_stopper(self):
        # Stop play the sound of electronic element
        self.Question_text.set("Sound END")
        self.Question.place(x=7 * self.width / 16, y=3 * self.height / 4)
        self.Question.config(fg="red", font=("Courier", 23, "bold"))
        if self.currentTrial[1] == '1':
            self.play_electronic_element.terminate()
            self.sound_stop = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f').split()[1]
        else:
            self.sound_stop = "-1"


if __name__ == "__main__":
    Experiment_Session()

