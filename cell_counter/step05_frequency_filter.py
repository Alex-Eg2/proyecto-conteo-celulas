import numpy as np
import cv2

from .step03_intensity import estiramiento_lineal


def filtro_pasa_bajas_fft(img, corte=90, mask=None):
    f = img.astype(np.float32)

    F = np.fft.fftshift(np.fft.fft2(f))

    filas, columnas = np.indices(f.shape)
    centro_fila = f.shape[0] // 2
    centro_col = f.shape[1] // 2

    dist = np.sqrt((filas - centro_fila)**2 + (columnas - centro_col)**2)

    mascara_freq = (dist <= corte).astype(np.float32)

    img_filtrada = np.abs(np.fft.ifft2(np.fft.ifftshift(F * mascara_freq)))
    img_filtrada = estiramiento_lineal(img_filtrada, mask)

    if mask is not None:
        img_filtrada = cv2.bitwise_and(img_filtrada, img_filtrada, mask=mask)

    return img_filtrada