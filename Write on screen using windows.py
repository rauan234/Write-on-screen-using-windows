from PyQt5.QtWidgets import QApplication, QMainWindow
from tkinter import Tk
from multiprocessing import Process
from time import sleep
from PIL import Image as img
import numpy as np
import math
import sys


WindowMakingDelay = 0.1
ApproxWindowsCount = 150
ApproxWindowsSpacing = 30
ScreenSize = (1600, 1000)
DrawingStyle = 'PyQT5'


# Create a window at position (x, y).
def make_window(x, y):
    if DrawingStyle == 'PyQT5':
        app = QApplication(sys.argv)
        ex = QMainWindow()
        ex.left = ex.top = ex.width = ex.height = 0
        ex.move(x, y)
        ex.show()
        sys.exit(app.exec_())
    else:  # DrawingStyle == 'tkinter'
        w = Tk()
        w.geometry('+{}+{}'.format(x, y))
        w.geometry('0x0')
        w.mainloop()


# Create windows at positions [(x_1, y_1), ..., (x_n, y_n)].
def make_windows(coords_list):
    for (x, y) in coords_list:
        p = Process(target=make_window, args=(x, y))
        p.start()

        sleep(WindowMakingDelay)


# Read an image.
def read_image_from_file(filename):
    return img.open(filename)


# Given an image, output an array of zeros and ones of the same size where 1 corresponds to "dark" and 0 to "light".
def convert_img_to_01(image):
    pixels = image.load()
    xsize, ysize = image.size

    out = np.zeros((ysize, xsize))

    for y in range(ysize):
        for x in range(xsize):
            rgb_sum = sum(pixels[x, y])

            out[y, x] = int(rgb_sum < 384)

    return out


# Given an array where 1 corresponds to dark pixels and 0 to light, output a list of coordinates for
# windows to be produced, so that the number of windows is roughly equal to desired_w_count.
def compute_windows_coords_list(array01, desired_w_count):
    n_black = np.sum(array01)  # number of dark pixels
    if n_black == 0:
        return []
    else:
        ysize, xsize = array01.shape

        # place windows at points whose coordinates are multiples of spacing
        spacing = math.ceil(math.sqrt(n_black / desired_w_count))
        coords_list = [(x, y) for y in range(0, ysize, spacing) for x in range(0, xsize, spacing) if array01[y, x]]

        # rescale the windows' positions to suit the desired dimensions
        scale_factor = ApproxWindowsSpacing / spacing
        scale_factor = min(scale_factor, ScreenSize[1] / ysize, ScreenSize[0] / xsize)
        rescaling_map = lambda coords: (round(coords[0] * scale_factor), round(coords[1] * scale_factor))
        coords_list = list(map(rescaling_map, coords_list))

        return coords_list


def main():
    image = read_image_from_file('Picture.jpg')
    blackwhite_array = convert_img_to_01(image)
    windows_to_be_made = compute_windows_coords_list(blackwhite_array, ApproxWindowsCount)
    make_windows(windows_to_be_made)

    print('Done')


if __name__ == '__main__':
    main()
