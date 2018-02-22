from random import shuffle


last_num = []
for i in range(54):
    if i < 27:
        last_num.append([1])
    else:
        last_num.append([2])


print last_num
last_num = shuffle(last_num)
print last_num