from gcodereader import gparser
import numpy as np
import matplotlib.pyplot as plt

path = r"trials\gcode\3DBenchy_0.2mm_PLA_MEGA0_1h48m.gcode"
parser = gparser()
pos = parser.cpos[:3]
queue = parser.parse(path)
points = np.zeros((3, len(queue)), float)
for move, i in zip(queue, range(len(queue))):
    points[0][i] = pos[0]
    points[1][i] = pos[1]
    points[2][i] = pos[2]
    pos += move[:3]
    # print(pos)

ax = plt.figure().add_subplot(projection="3d")
ax.plot(points[0], points[1], points[2],'o')
plt.axis('equal')
plt.show()
