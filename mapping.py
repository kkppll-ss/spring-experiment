import csv
import numpy as np
from jinja2 import Environment, FileSystemLoader

initial_value = float(input("give the initial value:"))
with open("spring.csv") as f:
    reader = csv.reader(f)
    l = np.array(list(reader), dtype=np.float64)

l[:, 0] -= initial_value
l[:, 0] = -l[:, 0]
l[:, 0] *= 10
i = np.argsort(l[:, 1])
l = l[i]
datas = []
for entry in zip(l[:-1], l[1:]):
    (y1, x1), (y2, x2) = entry
    x1, y1 = int(x1), float(y1)
    x2, y2 = int(x2), float(y2)
    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1
    datas.append({"x1": x1, "x2": x2, "k": k, "b": b})
env = Environment(loader=FileSystemLoader("."))
template = env.get_template('mapping_c.jinja2')
mapping = template.render(datas=datas)
with open("mapping.c", "w") as fh:
    fh.write(mapping)

