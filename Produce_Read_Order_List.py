# -*- coding: UTF-8 -*-

import random
# import ast

# Cognitive Load(2) * handness(2) * force profile(8) * 9 (repeated times)


class Produce_Read_Order_List:

    def __init__(self):
        self.pairs = []
        self.Commands = []
        self.User_Condition = {}
        self.Cognitive_Load = [0, 1]
        self.Handness = [0, 1]
        self.Force_Profile = ['FP01', 'FP02', 'FP03', 'FP04', 'FP05', 'FP06', 'FP07', 'FP08']
        self.Repeated_Times = ['RT01', 'RT02', 'RT03', 'RT04', 'RT05', 'RT06', 'RT07', 'RT08', 'RT09']
        self.read_line_counter = 0
        self.current_user_num = -1

        self.Users = [
                 "User1", "User2", "User3", "User4",
                 "User5", "User6", "User7", "User8",
                 "User9", "User10", "User11", "User12",
                 "User13", "User14", "User15", "User16"
                 ]

        self.condition_lookup_table = {
             'A': [0, 0],
             'B': [0, 1],
             'C': [1, 0],
             'D': [1, 1]
        }

        self.User_Condition["User1"] = ['A', 'D', 'C', 'B']
        self.User_Condition["User2"] = ['C', 'B', 'D', 'A']
        self.User_Condition["User3"] = ['C', 'B', 'D', 'A']
        self.User_Condition["User4"] = ['D', 'A', 'B', 'C']

        self.User_Condition["User5"] = ['B', 'C', 'D', 'A']
        self.User_Condition["User6"] = ['D', 'A', 'C', 'B']
        self.User_Condition["User7"] = ['C', 'B', 'A', 'D']
        self.User_Condition["User8"] = ['A', 'D', 'B', 'C']

        self.User_Condition["User9"] = ['D', 'C', 'A', 'B']
        self.User_Condition["User10"] = ['C', 'D', 'B', 'A']
        self.User_Condition["User11"] = ['B', 'A', 'D', 'C']
        self.User_Condition["User12"] = ['A', 'B', 'C', 'D']

        self.User_Condition["User13"] = ['D', 'C', 'B', 'A']
        self.User_Condition["User14"] = ['B', 'D', 'A', 'C']
        self.User_Condition["User15"] = ['C', 'A', 'D', 'B']
        self.User_Condition["User16"] = ['A', 'B', 'C', 'D']

    # Make pairs of Force Profile and Repeated times
    def make_pairs(self):
        for f in self.Force_Profile:
            for r in self.Repeated_Times:
                self.pairs.append([f, r])
        return self.pairs

    # Write order to current user's file,
    # User_Num: Range: [1-16],
    # Output File order list file: User_5_order_list.txt
    def start_up(self, user_num):
        self.current_user_num = user_num
        f = open("Order_List/User_"+str(self.current_user_num) + "_order_list.txt", "w")
        header = "Recognition_Load,Handness,Force_Profile,Repeated_Times\n"
        f.write(header)
        pairs = self.pairs
        pairs_list = [pairs[:], pairs[:], pairs[:], pairs[:]]
        user_name = "User" + str(self.current_user_num)
        Display_condition_order = self.User_Condition[user_name]

        for c, i in zip(Display_condition_order, pairs_list):
            while len(i) != 0:
                index = random.randrange(len(i))     # randomize the order of (force profile, repeated times) pairs
                f.write(str(self.condition_lookup_table[c][0]) + "," + str(self.condition_lookup_table[c][1]) + "," + i[index][0] + "," +i[index][1])
                f.write("\n")
                i.pop(index)

        print "User_Order_List Start Up Complete"

    # Store the parsed commands in internal Self.Commands variable
    def read_command(self, filename=None):
        counter = 0
        if filename is None:
            filename = "Order_List/User_" + str(self.current_user_num) + "_order_list.txt"
        with open(filename) as f:
            for line in f:
                if counter != 0 and len(line) != 0:
                    self.Commands.append(line[:-1].split(','))
                else:
                    counter += 1
        print "Commands stored in internal list"

    # Read the commands from self.Commands line by line
    def read_command_by_line(self):
        self.read_line_counter += 1
        return self.Commands[self.read_line_counter - 1]


# # Useage format
# cmd = Produce_Read_Order_List()
# cmd.make_pairs()
# cmd.start_up(16)
# cmd.read_command()
#
# for i in range(len(cmd.Commands)):
#     print cmd.read_command_by_line()


# print cmd.Commands
# print "******************************"
# print cmd.read_command_by_line()
# print cmd.read_command_by_line()
# print cmd.read_Command_by_line()
# print "******************************"
#
# for i in cmd.Commands:
#     print i