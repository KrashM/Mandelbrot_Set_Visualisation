from cmath import sqrt
import colorsys
import time
from threading import Thread
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt

WIDTH = 1920

x = -0.6
y = 0
xRange = 3.4
aspectRatio = 16/9

precission = 50

HEIGHT = round(WIDTH / aspectRatio)
yRange = xRange / aspectRatio
minX = x - xRange / 2
maxY = y + yRange / 2

_thread_count = multiprocessing.cpu_count()
colomnsPerThread = round(WIDTH / _thread_count)

img = np.full((HEIGHT, WIDTH), 255)

def colorAvg(distance):
    color = distance / precission
    rgb = colorsys.hsv_to_rgb(0, 0, 1 - color)
    return round((round(rgb[0] * 255) + round(rgb[1] * 255) + round(rgb[2] * 255)) / 3)

def fc(z: complex, c: complex, n: int) -> int:
    if (z*z.conjugate()).real >= 4 or n == precission:
        return n
    return fc(z*z + c, c, n + 1)

def draw(start: int, end: int):
    for i in range(HEIGHT):
        for j in range(start, end):
            x = minX + j * xRange / WIDTH
            y = maxY - i * yRange / HEIGHT
            z = complex(x, y)
            c = complex(x, y)
            color = colorAvg(fc(z, c, 0))
            img[i][j] = color

start = time.time()
threads = [ Thread(target=draw, args=(i * colomnsPerThread, (i + 1) * colomnsPerThread)) for i in range(_thread_count) ]
for i in range(_thread_count):
    threads[i].start()
for i in range(_thread_count):
    threads[i].join()
print(time.time() - start)
# plt.imshow(img)
# plt.axis('off')
# plt.show()
plt.imsave('{}x{}.png'.format(WIDTH, HEIGHT), img)
# im = Image.fromarray(img)
# im.save("{}x{}.png".format(WIDTH, HEIGHT))