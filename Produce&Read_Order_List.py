# -*- coding: UTF-8 -*-

import random

# Cognitive Load(2) * handness(2) * force profile(8) * 9 (repeated times)

Cognitive_Load = [0, 1]
Handness = [0, 1]
Force_Profile = [0, 1, 2, 3, 4, 5, 6, 7]
Repeated_Times = [0, 1, 2, 3, 4, 5, 6, 7, 8]

Users = [
         "User0", "User1", "User2", "User3",
         "User4", "User5", "User6", "User7",
         "User8", "User9", "User10", "User11",
         "User12", "User13", "User14", "User15"
         ]

User_Condition = {}

condition_lookup_table = {
     'A': [0,0],
     'B': [0,1],
     'C': [1,0],
     'D': [1,1]
}

def initial_user_condition():

    User_Condition["User0"] = ['A', 'D', 'C', 'B']
    User_Condition["User1"] = ['C', 'B', 'D', 'A']
    User_Condition["User2"] = ['C',	'B', 'D', 'A']
    User_Condition["User3"] = ['D',	'A', 'B', 'C']

    User_Condition["User4"] = ['B',	'C', 'D', 'A']
    User_Condition["User5"] = ['D',	'A', 'C', 'B']
    User_Condition["User6"] = ['C', 'B', 'A', 'D']
    User_Condition["User7"] = ['A',	'D','B', 'C']

    User_Condition["User8"] = ['D', 'C', 'A', 'B']
    User_Condition["User9"] = ['C', 'D', 'B', 'A']
    User_Condition["User10"] = ['B', 'A', 'D', 'C']
    User_Condition["User11"] = ['A', 'B', 'C', 'D']

    User_Condition["User12"] = ['D', 'C', 'B', 'A']
    User_Condition["User13"] = ['B', 'D', 'A', 'C']
    User_Condition["User14"] = ['C', 'A', 'D', 'B']
    User_Condition["User15"] = ['A', 'B', 'C', 'D']


def make_pairs(Force_Profile, Repeated_Times):
    pairs = []
    for f in Force_Profile:
        for r in Repeated_Times:
            pairs.append([f, r])
    return pairs


def start_up(user_name, pairs = []):
    f = open("current_user_order.txt", "w")
    header = ["Condition", "Force_Profile", "Repeated_Times"]
    f.write(str(header))
    f.write(str("\n"))
    pairs_list = [pairs[:], pairs[:], pairs[:], pairs[:]]
    user_name = "User" + str(user_name)

    Display_condition_order = User_Condition[user_name]

    for c, i in zip(Display_condition_order, pairs_list):
        while len(i) != 0:
            index = random.randrange(len(i))
            f.write(str([c, i[index][0], i[index][1]]) + '\n')
            i.pop(index)

    print "Start up complete"


# @param: list ['A', 4, 2] => [0,1,4,2] using the condition lookup table
def Parse_command(command):
    Cmd = []
    for i in range(len(command)):
        if i == 0:
            Cmd.append(condition_lookup_table[command[i]][0])
            Cmd.append(condition_lookup_table[command[i]][1])
        else:
            Cmd.append(command[i])
    return Cmd


def read_Command(filename):
    counter = 0
    Commands = []

    with open(filename) as f:
        for line in f:
            if counter != 0:
                temp = [line[2], line[6], line[9]]
                # print temp
                Commands.append(Parse_command(list(temp)))
            else:
                counter += 1

    return Commands

initial_user_condition()
pairs = make_pairs(Force_Profile, Repeated_Times)
start_up(2, pairs)
cmd = read_Command("current_user_order.txt")

# for i in cmd:
#     print i








