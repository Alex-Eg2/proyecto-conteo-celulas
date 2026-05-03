import os
import cv2
import matplotlib.pyplot as plt


def crear_carpeta(ruta):
    os.makedirs(ruta, exist_ok=True)


def cargar_imagen(ruta):
    img = cv2.imread(str(ruta))

    if img is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {ruta}")

    return img


def guardar_figura(num, titulo, img, output_dir, cmap=None, color="BGR", mostrar=False):
    crear_carpeta(output_dir)

    fig = plt.figure()

    if len(img.shape) == 2:
        plt.imshow(img, cmap=cmap if cmap else "gray")
    else:
        if color == "BGR":
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        else:
            plt.imshow(img)

    plt.title(titulo)
    plt.axis("off")

    nombre = f"{num:02d}_{titulo.lower().replace(' ', '_')}.png"
    ruta_salida = os.path.join(output_dir, nombre)

    plt.savefig(ruta_salida, bbox_inches="tight", dpi=150)

    if mostrar:
        plt.show()

    plt.close(fig)

    return ruta_salida


def guardar_comparacion(nombre_archivo, titulo_1, img_1, titulo_2, img_2,
                        output_dir, cmap="gray", mostrar=False):
    crear_carpeta(output_dir)

    fig = plt.figure(figsize=(8, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(img_1, cmap=cmap)
    plt.title(titulo_1)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(img_2, cmap=cmap)
    plt.title(titulo_2)
    plt.axis("off")

    ruta_salida = os.path.join(output_dir, nombre_archivo)
    plt.savefig(ruta_salida, bbox_inches="tight", dpi=150)

    if mostrar:
        plt.show()

    plt.close(fig)

    return ruta_salida