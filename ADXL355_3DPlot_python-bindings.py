""" 3D plot using ADXL355 and python bindings for libiio """

import iio
import sys
from matplotlib import pyplot as plt
from matplotlib import animation

my_uri = sys.argv[1] if len(sys.argv) >= 2 else None
print("uri: " + str(my_uri))
if my_uri is None:
    print("Connection error")
    exit(1)

ctx = iio.Context(my_uri)
if ctx is None:
    print("No context found")
    exit(1)
adxl355 = ctx.find_device('adxl355')

fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)

chx = adxl355.find_channel('accel_x').attrs
chy = adxl355.find_channel('accel_y').attrs
chz = adxl355.find_channel('accel_z').attrs


def init():
    ax.scatter(0, 0, 0, s=500, c='b')
    return fig,


def animate(i):
    ax.collections.clear()
    x = float(chx.get('raw').value) * float(chx.get('scale').value)
    y = float(chy.get('raw').value) * float(chy.get('scale').value)
    z = float(chz.get('raw').value) * float(chz.get('scale').value)
    ax.scatter(x, y, z, s=500, c='b')
    return fig,


ani = animation.FuncAnimation(fig, animate, init_func=init, interval=50)

plt.show()
