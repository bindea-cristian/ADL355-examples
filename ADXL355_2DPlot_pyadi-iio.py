""" 2D plot using ADXL355 and pyadi-iio """

import adi
import sys
from matplotlib import pyplot as plt
from matplotlib import animation

my_uri = sys.argv[1] if len(sys.argv) >= 2 else None
print("uri: " + str(my_uri))

if my_uri is None:
    print("Connection error")
    exit(1)

myacc = adi.adxl355(uri=my_uri)
myacc.rx_buffer_size = 32
myacc.rx_enabled_channels = [0, 1, 2]

fig = plt.figure(figsize=(5, 7))
fig.set_dpi(100)

xlim = 10
ylim = 10

ax1 = plt.axes(xlim=(-xlim, xlim), ylim=(-ylim, ylim))
circ1 = plt.Circle((0, 0), 1.3, color='r')
circ2 = plt.Circle((0, 0), 1.3, color='b')
circ3 = plt.Circle((0, 0), 1.3, color='g')


def init():
    circ1.center = (0, 0)
    circ2.center = (0, 0)
    circ3.center = (0, 0)
    ax1.add_patch(circ1)
    ax1.add_patch(circ2)
    ax1.add_patch(circ3)

    plt.hlines(0, 2, xlim, color='black')
    plt.hlines(0, -xlim, -2, color='black')
    plt.vlines(0, 2, ylim, color='black')
    plt.vlines(0, -ylim, -2, color='black')

    return circ1, circ2, circ3


def animate(i):
    x1 = myacc.accel_x.raw * myacc.accel_x.scale
    y1 = myacc.accel_y.raw * myacc.accel_y.scale
    x2 = myacc.accel_x.raw * myacc.accel_x.scale
    y2 = myacc.accel_z.raw * myacc.accel_z.scale
    x3 = myacc.accel_y.raw * myacc.accel_y.scale
    y3 = myacc.accel_z.raw * myacc.accel_z.scale

    circ1.center = (x1, y1)
    circ2.center = (x2, y2)
    circ3.center = (x3, y3)
    return circ1, circ2, circ3


anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               interval=20,
                               blit=True)

plt.show()
del myacc
