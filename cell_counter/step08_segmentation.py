import cv2
import numpy as np


def obtener_canales_lab(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(lab)

    return L, A, B


def segmentar_regiones(binaria, area_min=80, area_max=2500):
    num, etiquetas, stats, centroides = cv2.connectedComponentsWithStats(
        binaria,
        connectivity=8
    )

    regiones = []

    for i in range(1, num):
        area = stats[i, cv2.CC_STAT_AREA]

        if area_min <= area <= area_max:
            regiones.append({
                "area": int(area),
                "bbox": (
                    int(stats[i, cv2.CC_STAT_LEFT]),
                    int(stats[i, cv2.CC_STAT_TOP]),
                    int(stats[i, cv2.CC_STAT_WIDTH]),
                    int(stats[i, cv2.CC_STAT_HEIGHT])
                ),
                "centroide": (
                    int(centroides[i][0]),
                    int(centroides[i][1])
                )
            })

    return regiones


def detectar_leucocitos(L, A, B, mask_rec,
                        area_min=800,
                        kernel_close=15,
                        kernel_dilate=3,
                        iter_dilate=3):
    zona_morada = ((A > 132) & (B < 127) & (L > 35) & (L < 210)).astype(np.uint8) * 255
    zona_morada = cv2.bitwise_and(zona_morada, zona_morada, mask=mask_rec)

    zona_morada = cv2.morphologyEx(
        zona_morada,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_close, kernel_close))
    )

    num, etiquetas, stats, _ = cv2.connectedComponentsWithStats(
        zona_morada,
        connectivity=8
    )

    mask_leuco = np.zeros_like(zona_morada)

    for i in range(1, num):
        area = stats[i, cv2.CC_STAT_AREA]

        if area >= area_min:
            mask_leuco[etiquetas == i] = 255

    mask_leuco = cv2.dilate(
        mask_leuco,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_dilate, kernel_dilate)),
        iterations=iter_dilate
    )

    contornos, _ = cv2.findContours(
        mask_leuco,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    return mask_leuco, contornos