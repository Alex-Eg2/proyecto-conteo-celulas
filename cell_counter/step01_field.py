import cv2
import numpy as np


def mayor_componente(binaria):
    num, etiq, stats, _ = cv2.connectedComponentsWithStats(binaria, connectivity=8)

    if num <= 1:
        return binaria.copy()

    mayor = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])

    resultado = np.zeros_like(binaria)
    resultado[etiq == mayor] = 255

    return resultado


def detectar_campo(img, umbral_fondo=20, tam_kernel=15):
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, campo_bin = cv2.threshold(gris, umbral_fondo, 255, cv2.THRESH_BINARY)
    campo_bin = mayor_componente(campo_bin)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (tam_kernel, tam_kernel))
    campo_bin = cv2.morphologyEx(campo_bin, cv2.MORPH_CLOSE, kernel)

    return campo_bin


def recortar_campo(img, campo_bin):
    coords = cv2.findNonZero(campo_bin)

    if coords is None:
        raise ValueError("No se encontró el campo del microscopio.")

    x, y, w, h = cv2.boundingRect(coords)

    img_rec = img[y:y+h, x:x+w]
    mask_rec = campo_bin[y:y+h, x:x+w]

    img_campo = cv2.bitwise_and(img_rec, img_rec, mask=mask_rec)

    return img_campo, mask_rec