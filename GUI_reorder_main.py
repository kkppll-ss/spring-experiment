# -*- coding: UTF-8 -*-

import time
import Tkinter
import tkMessageBox
import Produce_Read_Order_list as Produce_Read_Order_List
from Play_electronic_element import play_electronic_element
from Tkinter import *
import ImageTk
import Image
import random
# from spring import Spring


class Experiment_Session:

    def __init__(self):
        # Set the basic params of windows
        self.root = Tkinter.Tk()
        self.root.title("Haptic Experiment")
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
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
            5: 'increasing',
            6: 'decreasing',
            7: 'click',
            8: 'drop'
        }

        self.cmd = Produce_Read_Order_List.Produce_Read_Order_List()  # Initiate list of command

        self.User_feel_FP = ""              # record the user's actual choice of haptic feeling
        self.global_times_counter = 0       # record the user's repeated times
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
        self.trackLength = 0                # track the length of the sound playlist
        self.write_info = ""                # Information written to output file
        self.show_info = ""                 # Information showed on the panel
        self.pin_height = ""                # Information of the pin height

        # Switch between show debug and not show
        self.show_debug = False

        self.TrialInfo = Tkinter.StringVar(value='')                # Trial information
        self.Answer = Tkinter.StringVar(value='')                   # User answer
        self.Question_text = Tkinter.StringVar(value='')            # Text of Question
        self.Question_choice_row_1 = Tkinter.StringVar(value='')    # First row of choice of question
        self.Question_choice_row_2 = Tkinter.StringVar(value='')    # Second row of choice of question
        self.Question_choice_row_3 = Tkinter.StringVar(value='')    # Third row of choice of question
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

        self.Info_Header = Label(self.root, text="Trial\tRecongition Load\tHandness\tComponent", anchor=W)
        self.Info_Header.config(font=("Courier", 12, "bold"))

        self.Info = Label(self.root, textvariable=self.TrialInfo, anchor=W)
        self.Info.config(font=("Courier", 12, "bold"))

        # Set up and place the images at the second level
        img_1 = Image.open('img/F01.jpg')
        img_1 = img_1.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_1 = ImageTk.PhotoImage(img_1)

        img_2 = Image.open('img/F02.jpg')
        img_2 = img_2.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_2 = ImageTk.PhotoImage(img_2)

        img_3 = Image.open('img/F03.jpg')
        img_3 = img_3.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_3 = ImageTk.PhotoImage(img_3)

        img_4 = Image.open('img/F04.jpg')
        img_4 = img_4.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_4 = ImageTk.PhotoImage(img_4)

        img_5 = Image.open('img/F05.jpg')
        img_5 = img_5.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_5 = ImageTk.PhotoImage(img_5)

        img_6 = Image.open('img/F06.jpg')
        img_6 = img_6.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_6 = ImageTk.PhotoImage(img_6)

        img_7 = Image.open('img/F07.jpg')
        img_7 = img_7.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_7 = ImageTk.PhotoImage(img_7)

        img_8 = Image.open('img/F08.jpg')
        img_8 = img_8.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_8 = ImageTk.PhotoImage(img_8)

        col_x_1 = w / 15
        col_x_2 = 2 * w/15 + w / 6
        col_x_3 = 3 * w/15 + 2 * w / 6
        col_x_4 = 4 * w/15 + 3 * w / 6

        label_level_1_y = top_entry_y + 2 * h/20
        label_level_2_y = top_entry_y + 4 * h / 20 + h / 6

        img_level_1_y = top_entry_y + 3 * h/20
        img_level_2_y = top_entry_y + 5 * h / 20 + h/6

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
        self.FP4.place(x=col_x_4, y=label_level_1_y)
        self.FP4.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_4).place(x=col_x_4, y=img_level_1_y)

        self.FP5 = Label(self.root, text="5. increasing", fg='blue')
        self.FP5.place(x=col_x_1, y= label_level_2_y)
        self.FP5.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_5).place(x=col_x_1, y=img_level_2_y)

        self.FP6 = Label(self.root, text="6. decreasing", fg='blue')
        self.FP6.place(x=col_x_2, y=label_level_2_y)
        self.FP6.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_6).place(x=col_x_2, y=img_level_2_y)

        self.FP7 = Label(self.root, text="7. click", fg='blue')
        self.FP7.place(x=col_x_3, y=label_level_2_y)
        self.FP7.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_7).place(x=col_x_3, y=img_level_2_y)

        self.FP8 = Label(self.root, text="8. drop", fg='blue')
        self.FP8.place(x=col_x_4, y=label_level_2_y)
        self.FP8.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_8).place(x=col_x_4, y=img_level_2_y)

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

        self.Choice_row_1 = Label(self.root, textvariable=self.Question_choice_row_1)
        self.Choice_row_2 = Label(self.root, textvariable=self.Question_choice_row_2)
        self.Choice_row_3 = Label(self.root, textvariable=self.Question_choice_row_3)

        self.User_Answer = Tkinter.Label(self.root, text='Answer: ', fg="blue")
        self.User_Answer.place(x=w/2 - w/8, y=7*h/8)
        self.User_Answer.config(font=("Courier", 20, "bold"))
        self.entry_Answer = Tkinter.Entry(self.root, width=80, textvariable=self.Answer)
        self.entry_Answer.place(x=w/2 - w/25, y=7*h/8, width=w / 12, height=h / 25)

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
            else:
                self.cmd.start_up(int(self.user_num))  # Produce commands by user number
                self.cmd.read_command()           # Read commands => commands
                # write the head information to the first line in the file
                self.outputfile = open("Records/User_" + str(self.user_num) + "_record.txt", "w")
                self.outputfile.write("User_num,User_name,User_age,User_gender,Trials,Pin_height,Recognition_Load,Handness,Force_Profile,Repeated_Times,Duration_Time,User_Choice,Haptic_Choice_Correctness, ask_last_num,actual_electronic_element,user_RL_Choice,Recognition_Load_Correctness\n")
                self.outputfile.close()

            # Re-open the output file again for later record useage
            self.outputfile = open("Records/User_" + str(self.user_num) + "_record.txt", "a")
        else:
            tkMessageBox.showinfo('Error', message='Please enter an valid number[0-12]')

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
        self.Info_Header.place(x=23 * self.width / 80, y=self.height / 80, width=29 * self.width / 64, height=self.height / 25)
        self.Info_Header.config(bg="red", fg="white")
        self.Info_Header.config(font=("Courier", 15, "bold"))

        self.Info.place(x=23 * self.width/80, y=self.height/80 + self.height/22, width=29 * self.width / 64, height=self.height/25)
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
                tkMessageBox.showinfo('Warning', message='Press [Enter] to Start a trial before proceed')
                return

            # Press Space more than twice without press [Enter]
            if self.PressSpaceTwice is True:
                tkMessageBox.showinfo('Warning', message='Enter the Haptic Feel before Proceed')
                return

            print "Space Entered"
            if self.SpacePressTime % 2 == 0:
                self.start = int(round(time.time() * 1000))
                self.Question_text.set("Haptic Test START")
                self.Question.place(x=6 * self.width / 16, y=3 * self.height / 4)
                self.Question.config(font=("Courier", 23, "bold"))
                self.Question.config(fg="green")

                # Start to play the electronic element
                if self.currentTrial[1] == '1':
                    self.play_electronic_element = play_electronic_element()
                    self.play_electronic_element.start()

                # Create thread for handling haptic Spring
                # self.spring = Spring(self.Position_Info.set)
                # self.spring.set_profile(self.currentTrial[2])
                # self.spring.start()
            else:
                # Stop the movement of Haptic Spring
                # self.spring.terminate()

                # Stop play the sound of electronic element
                if self.currentTrial[1] == '1':
                    self.play_electronic_element.terminate()
                    self.trackLength = len(self.play_electronic_element.traceList)

                self.deltatime = int(round(time.time() * 1000)) - self.start
                self.Question_text.set("Haptic Test END")
                self.Question.place(x=7 * self.width / 16, y=3 * self.height / 4)
                self.Question.config(fg="red", font=("Courier", 23, "bold"))
                self.Question.after(500, lambda: self.Question_text.set(""))

                self.Question.after(500, lambda: self.Question_text.set("Please Select a Haptic Feel"))
                self.Question.place(x= 5 * self.width / 16, y=3 * self.height / 4)
                self.Question.config(font=("Courier", 23, "bold"), fg="blue")
                self.PressSpaceTwice = True
            self.SpacePressTime += 1

    # [Enter] Press for 1. Show a Trial Information 2. Show a electronic elements
    def EnterPress(self, event):

        # Error Handling
        if self.user_num == -1 or self.user_name == "" or self.user_gender == "" or self.user_age == "":
            tkMessageBox.showinfo('Warning', message='Please Complete the Personal Info before proceed')
            return

        # the first time press [Enter]: show a Trial Information
        if self.EnterPressTime == 0:
            self.currentTrial = self.cmd.read_command_by_line()
            print self.currentTrial

            # Current/Total times
            self.write_info += str(self.user_num)+","+self.user_name+","+str(self.user_age)+","+self.user_gender+","

            if self.startTrialNum == 0:
                current_time = self.global_times_counter + 1
            else:
                current_time = self.global_times_counter + self.startTrialNum

            self.show_info += "  "+str(current_time) + "\t   "
            self.write_info += str(current_time) + ","

            for i in range(len(self.currentTrial)):
                if i == 0:
                    self.pin_height = self.currentTrial[i]
                    self.write_info += str(self.pin_height)+","
                if i == 1:
                    if self.currentTrial[i] == '1':
                        self.show_info += "  True\t\t"
                        self.write_info += "1,"
                    else:
                        self.show_info += "  False\t\t"
                        self.write_info += "0,"
                if i == 2:
                    if self.currentTrial[i] == '1':
                        self.show_info += "Dominant\t   "
                        self.write_info += "1,"
                    else:
                        self.show_info += "Non-Dominant\t   "
                        self.write_info += "0,"
                if i == 3:
                    self.write_info += self.currentTrial[i] + ","
                #   self.show_info += self.currentTrial[i]+"\t\t    "
                    self.Debug_Info.set("FP: " + self.currentTrial[i])
                if i == 4:
                    self.show_info += self.currentTrial[i]
                    self.write_info += self.currentTrial[i] + ","

            self.TrialInfo.set(self.show_info)
            self.global_times_counter += 1
            self.show_info = ""

        elif self.EnterPressTime % 2 == 1:

            # Unfinished Haptic Test
            if self.PressSpaceTwice is False:
                tkMessageBox.showinfo('Warning', message='Finish Haptic Test before proceed Press [Space]')
                return

            if len(self.entry_Answer.get()) == 0:
                tkMessageBox.showinfo('Warning', message='Enter your actual feel before proceed')
                return
            else:
                if self.entry_Answer.get().strip().isdigit() and 0 < int(self.entry_Answer.get().strip()) < 9:
                    self.User_feel_FP = self.haptic_feel_lookup[int(self.entry_Answer.get())]
                    result = tkMessageBox.askyesno(title='Notice', message='Your Haptic Choice: ' + self.User_feel_FP +'\nCan you confirm ?')
                    if result is True:
                        pass
                    else:
                        return
                else:
                    tkMessageBox.showinfo(title='Notice', message='Your Choice MUST BE Integer in [1-8]')
                    return

                self.Answer.set("")

                # Show the recognition load question
                if self.currentTrial[1] == '1':
                    self.ask_last_num = random.randrange(1, 4)  # random number for quiz of last element

                    if self.ask_last_num > self.trackLength:
                        self.ask_last_num = self.trackLength

                    self.Question_text.set("Select the Last " + str(self.ask_last_num) + "th Electronic Element\n")
                    self.Question_choice_row_1.set("  1. Capacitor\t\t   2. Diode")
                    self.Question_choice_row_2.set("  3. Integrate Circuit     4. LED(light-Emitting Diode)")
                    self.Question_choice_row_3.set("  5. Resistor\t           6. Transistor")

                    base_question_x = 19*self.width/64
                    base_question_y = 11*self.height/16
                    base_question_y_row_1 = base_question_y + 30
                    base_question_y_row_2 = base_question_y_row_1 + 30
                    base_question_y_row_3 = base_question_y_row_2 + 30

                    self.Question.place(x=base_question_x, y=base_question_y, anchor=W)
                    self.Choice_row_1.place(x=base_question_x, y=base_question_y_row_1, anchor=W)
                    self.Choice_row_2.place(x=base_question_x, y=base_question_y_row_2, anchor=W)
                    self.Choice_row_3.place(x=base_question_x, y= base_question_y_row_3, anchor=W)
                    self.Question.config(font=("Courier", 20, "bold"), fg="red")
                    self.Choice_row_1.config(font=("Courier", 20, "bold"), fg="black")
                    self.Choice_row_2.config(font=("Courier", 20, "bold"), fg="black")
                    self.Choice_row_3.config(font=("Courier", 20, "bold"), fg="black")
                else:
                    self.Question_text.set("No Question just Press [Enter] to Proceed")

        # Write the current user trial data information to output file
        # and choice and show a trial Information
        elif self.EnterPressTime % 2 == 0:
            # Recognition Load question answer
            if self.currentTrial[1] == '1':
                if len(self.entry_Answer.get()) == 0:
                    tkMessageBox.showinfo('Warning', message='Select the element you hear before proceed')
                    return
                else:
                    if self.entry_Answer.get().strip().isdigit() and 0 < int(self.entry_Answer.get().strip()) < 7:
                        self.user_choice = int(self.entry_Answer.get())
                    else:
                        tkMessageBox.showinfo(title='Notice', message='Your Choice MUST BE Integer in [1-6]')
                        return

                result = tkMessageBox.askyesno('Notice', message='Your Recognition Load Choice: ' + str(self.user_choice) + '\nCan you confirm ?')
                if result is True:
                    pass
                else:
                    return
            else:
                self.user_choice = -1

            self.Question_text.set("")
            self.Question_choice_row_1.set("")
            self.Question_choice_row_2.set("")
            self.Question_choice_row_3.set("")
            self.Answer.set("")

            self.write_info += str(self.deltatime) + ","
            self.write_info += str(self.User_feel_FP) + ","
            self.write_info += str(self.User_feel_FP == self.currentTrial[3]) + ","
            print self.User_feel_FP+","+self.currentTrial[3]+","+str(self.User_feel_FP == self.currentTrial[3])
            self.write_info += str(self.ask_last_num) + ","

            if self.currentTrial[1] == '1':
                self.write_info += str(self.play_electronic_element.last_i_th(self.ask_last_num)) + ","
                self.write_info += str(self.user_choice) + ","
                self.write_info += str(int(self.user_choice) == int(self.play_electronic_element.last_i_th(self.ask_last_num))) + "\n"
            else:
                self.write_info += str(-1) + ","
                self.write_info += str(self.user_choice) + ","
                self.write_info += str(-1) + "\n"

            self.outputfile.write(self.write_info)
            self.outputfile.flush()
            self.write_info = ""

            # When the trial times reach the end
            if self.global_times_counter == len(self.cmd.Commands):
                tkMessageBox.showinfo('Notice', message='Haptic Test End, Thank you!!')
                return

            # Begin the next trial
            self.currentTrial = self.cmd.read_command_by_line()
            print self.currentTrial

            # Current/Total times
            self.write_info += str(self.user_num)+","+self.user_name+","+str(self.user_age)+","+self.user_gender+","

            if self.startTrialNum == 0:
                current_time = self.global_times_counter + 1
            else:
                current_time = self.global_times_counter + self.startTrialNum

            self.show_info += str(current_time) + "\t\t"
            self.write_info += str(current_time) + ","

            for i in range(len(self.currentTrial)):
                if i == 0:
                    self.pin_height = self.currentTrial[i]
                    self.write_info += str(self.pin_height) + ","
                if i == 1:
                    if self.currentTrial[i] == '1':
                        self.show_info += "True\t\t"
                        self.write_info += "1,"
                    else:
                        self.show_info += "False\t\t"
                        self.write_info += "0,"
                if i == 2:
                    if self.currentTrial[i] == '1':
                        self.show_info += "True\t\t"
                        self.write_info += "1,"
                    else:
                        self.show_info += "False\t\t"
                        self.write_info += "0,"
                if i == 3:
                    # self.show_info += self.currentTrial[i] + "\t\t"
                    self.Debug_Info.set("FP: " + self.currentTrial[i])
                    self.write_info += self.currentTrial[i] + ","
                if i == 4:
                    self.show_info += self.currentTrial[i]
                    self.write_info += self.currentTrial[i] + ","

            self.PressSpaceTwice = False
            self.TrialInfo.set(self.show_info)
            self.global_times_counter += 1
            self.show_info = ""

        self.EnterPressTime += 1


if __name__ == "__main__":
    Experiment_Session()
