""" 3D plot using ADXL355 and pyadi-iio """

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

fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)


def init():
    ax.scatter(0, 0, 0, s=500, c='b')
    return fig,


def animate(i):
    ax.collections.clear()
    x = myacc.accel_x.raw * myacc.accel_x.scale
    y = myacc.accel_y.raw * myacc.accel_y.scale
    z = myacc.accel_z.raw * myacc.accel_z.scale
    ax.scatter(x, y, z, s=500, c='b')
    return fig,


ani = animation.FuncAnimation(fig, animate, init_func=init, interval=50)

plt.show()
