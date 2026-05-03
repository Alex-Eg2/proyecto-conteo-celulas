import cv2
import numpy as np


def otsu_manual(img, mask=None):
    if mask is not None:
        pixeles = img[mask > 0]
    else:
        pixeles = img.flatten()

    hist = np.zeros(256, dtype=np.float64)

    for v in pixeles:
        hist[int(v)] += 1

    total = pixeles.size
    suma_total = np.sum(np.arange(256) * hist)

    peso_fondo = 0.0
    suma_fondo = 0.0

    var_max = 0.0
    umbral = 0

    for t in range(256):
        peso_fondo += hist[t]

        if peso_fondo == 0:
            continue

        peso_objeto = total - peso_fondo

        if peso_objeto == 0:
            break

        suma_fondo += t * hist[t]

        media_fondo = suma_fondo / peso_fondo
        media_objeto = (suma_total - suma_fondo) / peso_objeto

        var_entre_clases = peso_fondo * peso_objeto * (media_fondo - media_objeto)**2

        if var_entre_clases > var_max:
            var_max = var_entre_clases
            umbral = t

    binaria = np.zeros_like(img, dtype=np.uint8)
    binaria[img <= umbral] = 255

    if mask is not None:
        binaria = cv2.bitwise_and(binaria, binaria, mask=mask)

    return umbral, binaria


def limpiar_binaria(binaria):
    binaria = cv2.morphologyEx(
        binaria,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    )

    binaria = cv2.morphologyEx(
        binaria,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    )

    return binaria