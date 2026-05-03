import cv2


def convertir_grises(img, mask=None):
    if len(img.shape) == 2:
        gris = img.copy()
    else:
        gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if mask is not None:
        gris = cv2.bitwise_and(gris, gris, mask=mask)

    return gris