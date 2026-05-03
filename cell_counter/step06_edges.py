import cv2
import numpy as np


def convolve2d_manual(img, kernel):
    kh, kw = kernel.shape

    rel = np.pad(
        img,
        ((kh // 2, kh // 2), (kw // 2, kw // 2)),
        mode="edge"
    )

    sal = np.zeros_like(img, dtype=np.float32)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            sal[i, j] = np.sum(rel[i:i+kh, j:j+kw] * kernel)

    return sal


def sobel(img, mask=None, ratio=0.08):
    kx = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32)

    ky = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ], dtype=np.float32)

    gx = convolve2d_manual(img.astype(np.float32), kx)
    gy = convolve2d_manual(img.astype(np.float32), ky)

    mag = np.sqrt(gx**2 + gy**2)

    if mag.max() != 0:
        mag = (mag / mag.max() * 255).astype(np.uint8)
    else:
        mag = mag.astype(np.uint8)

    if mask is not None:
        mag = cv2.bitwise_and(mag, mag, mask=mask)

    bordes = np.zeros_like(mag)
    bordes[mag >= int(ratio * 255)] = 255

    if mask is not None:
        bordes = cv2.bitwise_and(bordes, bordes, mask=mask)

    return mag, bordes