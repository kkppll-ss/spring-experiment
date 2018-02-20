# -*- coding: UTF-8 -*-


def Recover_from_Record(filename=None):

    RL_correct = 0
    RL_total = 0
    if not filename:
        f = open("Records/User_" + str(4) + "_record.txt", "r")
    else:
        f = open(filename, "r")

    read_counter = 0

    for i in f:
        i = i.strip('\n').split(',')
        # print i
        if read_counter == 0:
            read_counter += 1
        else:
            if i[-5] == '1':
                RL_correct += 1
                RL_total += 1
            elif i[-5] == '0':
                RL_total += 1

    return RL_correct, RL_total


if __name__ == "__main__":
    print Recover_from_Record()
