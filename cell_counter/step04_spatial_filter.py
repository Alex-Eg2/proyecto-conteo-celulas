import numpy as np


def filtro_promediador(img, k=5):
    if k % 2 == 0:
        raise ValueError("El tamaño del kernel debe ser impar.")

    pad = k // 2

    rel = np.pad(img, pad_width=pad, mode="edge")
    sal = np.zeros_like(img, dtype=np.float32)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            sal[i, j] = np.mean(rel[i:i+k, j:j+k])

    return np.clip(sal, 0, 255).astype(np.uint8)