import cv2
import numpy as np


def conteo_hough(img_gris, zona_busqueda,
                 dp=1.2,
                 min_dist=16,
                 param1=80,
                 param2=18,
                 min_rad=6,
                 max_rad=18):
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))

    img_clahe = clahe.apply(img_gris)
    img_clahe = cv2.bitwise_and(img_clahe, img_clahe, mask=zona_busqueda)

    suavizada = cv2.GaussianBlur(img_clahe, (5, 5), 1.5)
    suavizada = cv2.bitwise_and(suavizada, suavizada, mask=zona_busqueda)

    circulos = cv2.HoughCircles(
        suavizada,
        cv2.HOUGH_GRADIENT,
        dp=dp,
        minDist=min_dist,
        param1=param1,
        param2=param2,
        minRadius=min_rad,
        maxRadius=max_rad
    )

    detectados = []

    if circulos is not None:
        circulos = np.round(circulos[0, :]).astype("int")

        for x, y, r in circulos:
            dentro = (
                0 <= y < zona_busqueda.shape[0] and
                0 <= x < zona_busqueda.shape[1]
            )

            if dentro and zona_busqueda[y, x] != 0:
                detectados.append((int(x), int(y), int(r)))

    return detectados, img_clahe, suavizada