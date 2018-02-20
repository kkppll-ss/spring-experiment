  # -*- coding: UTF-8 -*-

import random


# total = 3(Pin Height) x 2(Recognition Load) x 2(Handness) x 8(Force Profile) x 3(Pin Height specific component)
class Produce_Read_Order_List:

    def __init__(self):
        self.Commands = []
        self.Cognitive_Load = [0, 1]
        self.Handness = [0, 1]
        self.Pin_Height = [0, 1, 2]
        self.Force_Profile = ['empty', 'low', 'high', 'medium', 'increasing', 'decreasing', 'click', 'drop']
        self.Electronic_Element = {'A': ['1', '2', '3'],
                                   'B': ['4', '5', '6'],
                                   'C': ['7', '8', '9']}
        self.Electronic_Element_Component_lookup = {
            '1': '光敏电阻',
            '2': '发光二极管',
            '3': '电阻',
            '4': '场效应管',
            '5': '三极管',
            '6': '电容',
            '7': '芯片',
            '8': '电位器',
            '9': '跳线',
        }
        self.read_line_counter = 0
        self.current_user_num = -1
        self.User_Condition = {}
        self.cognitive_load_handness = []

        self.Users = [
            "User1", "User2", "User3", "User4",
            "User5", "User6", "User7", "User8",
            "User9", "User10", "User11", "User12",
        ]

        # Condition Table for pin height
        self.condition_lookup_table = ['A', 'B', 'C']

        self.User_Condition["User1"] = ['C', 'B', 'A']
        self.User_Condition["User2"] = ['A', 'C', 'B']
        self.User_Condition["User3"] = ['B', 'A', 'C']
        self.User_Condition["User4"] = ['A', 'C', 'B']

        self.User_Condition["User5"] = ['B', 'A', 'C']
        self.User_Condition["User6"] = ['C', 'B', 'A']
        self.User_Condition["User7"] = ['C', 'A', 'B']
        self.User_Condition["User8"] = ['A', 'B', 'C']

        self.User_Condition["User9"] = ['B', 'C', 'A']
        self.User_Condition["User10"] = ['A', 'B', 'C']
        self.User_Condition["User11"] = ['C', 'A', 'B']
        self.User_Condition["User12"] = ['B', 'C', 'A']

        # Make pairs of Force Profile and Repeated times
    def make_pairs(self, list_1, list_2):
        pairs = []
        for f in list_1:
            for r in list_2:
                pairs.append([f, r])
        return pairs

    # Write order to current user's file,
    # User_Num: Range: [1-12],
    # Output File order list file: User_4_order_list.txt
    def start_up(self, user_num):
        self.current_user_num = user_num
        user_name = "User" + str(self.current_user_num)

        force_profile_electronic_component = {}
        force_profile_electronic_component_list = {}

        # cognitive_load_handness pairs 2x2
        # cognitive_load_handness pairs list 3x2x2 
        cognitive_load_handness = self.make_pairs(self.Cognitive_Load, self.Handness)
        cognitive_load_handness_pairs_list = [cognitive_load_handness[:], cognitive_load_handness[:], cognitive_load_handness[:]]

        # force_profile_electronic_component pairs 8x3
        for i in self.condition_lookup_table:
            force_profile_electronic_component[i] = self.make_pairs(self.Force_Profile, self.Electronic_Element[i])

        pin_condition_order = self.User_Condition[user_name]
        for i in pin_condition_order:
            force_profile_electronic_component_list[i] = [force_profile_electronic_component[i][:], force_profile_electronic_component[i][:], force_profile_electronic_component[i][:], force_profile_electronic_component[i][:]]

        f = open("Order_List/User_" + str(self.current_user_num) + "_order_list.txt", "w")
        header = "Pin Height,Recognition_Load,Handness,Force_Profile,Electronic_Component\n"
        f.write(header)

        for i in range(len(pin_condition_order)):
            c = 3
            while len(cognitive_load_handness_pairs_list[i]) != 0:
                index_clh = random.randrange(len(cognitive_load_handness_pairs_list[i]))
                cognitive_load_handness_pair = cognitive_load_handness_pairs_list[i][index_clh]

                fp_ec = force_profile_electronic_component_list[pin_condition_order[i]][c]
                while len(fp_ec) != 0:
                    index_fp_ec = random.randrange(len(fp_ec))
                    force_profile_electronic_component_pair = fp_ec[index_fp_ec]
                    f.write(str(pin_condition_order[i]) + "," + str(cognitive_load_handness_pair[0]) + "," + str(cognitive_load_handness_pair[1]) + "," + str(force_profile_electronic_component_pair[0]) + "," + str(force_profile_electronic_component_pair[1]))
                    f.write("\n")
                    fp_ec.pop(index_fp_ec)

                c -= 1
                cognitive_load_handness_pairs_list[i].pop(index_clh)

        print "\n**User_Order_List Start Up Complete!!\n"

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
        print "**Commands stored in internal list**"

    # Read the commands from self.Commands line by line
    def read_command_by_line(self):
        self.read_line_counter += 1
        return self.Commands[self.read_line_counter - 1]


if __name__ == "__main__":
    cmd = Produce_Read_Order_List()
    cmd.start_up(4)
    cmd.read_command()

# for i in range(len(cmd.Commands)):
#     print cmd.read_command_by_line()


