import csv
import numpy as np
from matplotlib import pyplot as plt

with open("log.csv") as f:
    reader = csv.reader(f)
    l = list(reader)

for row in l:
    for i in range(len(row)):
        row[i] = float(row[i])
l = np.array(l)
print l
time = l[:, 0]
force = l[:, 1] * 3
x_to_k = l[:, 2]
x = l[:, 3]
setpoint = l[:, 4]
proximity = l[:, 5]
k = l[:, 6]
output = l[:, 7]
plt.subplot(311)
plt.plot(x_to_k, k, "go", label="k")
plt.legend()
plt.subplot(312)
plt.plot(time, x, "go", label="expected")
plt.plot(time, setpoint, "gx", label="actual_expected")
plt.plot(time, proximity, "yo", label="actual")
plt.plot(time, force / k * 1000, "bx", label="equalibrium")
plt.plot(time, output, 'b-', label="output")
plt.plot(time, force * 100, "bo", label="F * 100")
plt.legend()
plt.subplot(313)
plt.plot(time, force * 100, "bx", label="F * 100")
plt.legend()
plt.show()