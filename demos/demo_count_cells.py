from pathlib import Path
import sys

# Agrega la carpeta raíz del proyecto al path para que Python encuentre cell_counter
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from cell_counter.step10_pipeline import procesar_imagen


#%% Carpetas principales

IMAGES_DIR = BASE_DIR / "images"
OUTPUTS_DIR = BASE_DIR / "outputs"

EXTENSIONES_VALIDAS = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]


#%% Funciones auxiliares del demo

def listar_imagenes(images_dir):
    imagenes = []

    for ext in EXTENSIONES_VALIDAS:
        imagenes.extend(images_dir.glob(f"*{ext}"))
        imagenes.extend(images_dir.glob(f"*{ext.upper()}"))

    imagenes = sorted(set(imagenes), key=lambda p: p.name.lower())

    return imagenes


def buscar_imagen(nombre, images_dir):
    entrada = Path(nombre.strip())

    if entrada.suffix:
        # Si el usuario escribe sample_01.jpg
        ruta = images_dir / entrada.name

        if ruta.exists():
            return ruta

    else:
        # Si el usuario escribe solo sample_01, busca con extensiones válidas
        for ext in EXTENSIONES_VALIDAS:
            ruta = images_dir / f"{entrada.name}{ext}"

            if ruta.exists():
                return ruta

            ruta_mayus = images_dir / f"{entrada.name}{ext.upper()}"

            if ruta_mayus.exists():
                return ruta_mayus

    raise FileNotFoundError(f"No se encontró la imagen: {nombre}")


#%% Programa principal

print("\nIMÁGENES DISPONIBLES EN LA CARPETA images/")
print("-" * 50)

imagenes = listar_imagenes(IMAGES_DIR)

if len(imagenes) == 0:
    print("No hay imágenes en la carpeta images/")
    print(f"Agrega una imagen en: {IMAGES_DIR}")
    raise SystemExit

for img in imagenes:
    print(f"- {img.name}")

print("-" * 50)

nombre_imagen = input("\nEscribe el nombre de la imagen a procesar: ")

img_path = buscar_imagen(nombre_imagen, IMAGES_DIR)

# La carpeta de salida se llamará igual que la imagen, sin extensión
output_dir = OUTPUTS_DIR / img_path.stem

print("\nProcesando imagen...")
print(f"Imagen seleccionada : {img_path.name}")
print(f"Carpeta de salida   : {output_dir}")
print("\nCierra cada ventana de imagen para continuar con el siguiente paso.\n")

resultados = procesar_imagen(
    img_path=img_path,
    output_dir=output_dir,
    guardar_pasos=True,
    mostrar_pasos=True
)

print("\n" + "=" * 50)
print("RESULTADOS DEL PROCESAMIENTO")
print("=" * 50)
print(f"Imagen procesada    : {resultados['imagen']}")
print(f"Umbral Otsu LAB A   : {resultados['umbral_otsu_lab_a']}")
print(f"Regiones validas    : {resultados['regiones_validas']}")
print(f"Leucocitos          : {resultados['leucocitos']}")
print(f"Eritrocitos Hough   : {resultados['eritrocitos_hough']}")
print(f"Salidas guardadas   : {resultados['output_dir']}")
print("=" * 50)