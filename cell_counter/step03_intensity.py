import numpy as np


def estiramiento_lineal(img, mask=None):
    f = img.astype(np.float32)

    if mask is not None:
        pixeles = f[mask > 0]

        if pixeles.size == 0:
            return img.astype(np.uint8)

        a = pixeles.min()
        b = pixeles.max()

        if b == a:
            return img.astype(np.uint8)

        temp = ((f - a) / (b - a)) * 255
        temp = np.clip(temp, 0, 255).astype(np.uint8)

        salida = np.zeros_like(temp, dtype=np.uint8)
        salida[mask > 0] = temp[mask > 0]

        return salida

    a = f.min()
    b = f.max()

    if b == a:
        return img.astype(np.uint8)

    salida = ((f - a) / (b - a)) * 255
    salida = np.clip(salida, 0, 255).astype(np.uint8)

    return salida