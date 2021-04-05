import numpy as np
import cv2

def square_fit(img):
    s = max(img.shape[0:2])

    # Creating a dark square with NUMPY
    f = np.zeros((s, s, 3), np.uint8)

    # Getting the centering position
    ax, ay = (s - img.shape[1]) // 2, (s - img.shape[0]) // 2

    # Pasting the 'image' in a centering position
    f[ay:img.shape[0] + ay, ax:ax + img.shape[1]] = img
    f = cv2.resize(f, (720, 720))
    return f