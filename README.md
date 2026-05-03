# Proyecto 1 - Conteo automático de células en imágenes microscópicas

Este proyecto consiste en una librería en Python para procesar imágenes microscópicas y realizar el conteo automático de células. El sistema aplica preprocesamiento, segmentación, detección de bordes, umbralización y conteo mediante Transformada de Hough.

## Objetivo

Diseñar e implementar una librería en Python capaz de detectar, segmentar y contar células en imágenes microscópicas, integrando técnicas de procesamiento digital de imágenes.

## Técnicas utilizadas

El flujo de procesamiento incluye:

1. Lectura de imagen.
2. Detección del campo circular del microscopio.
3. Recorte de la zona útil.
4. Conversión a escala de grises.
5. Estiramiento lineal de contraste con máscara.
6. Filtrado espacial mediante filtro promediador.
7. Filtrado en frecuencia mediante filtro pasa-bajas FFT.
8. Detección de bordes con operador Sobel.
9. Umbralización mediante método de Otsu.
10. Segmentación por regiones conectadas.
11. Detección y exclusión de leucocitos.
12. Conteo final mediante Transformada de Hough.

## Estructura del proyecto

```text
proyecto_conteo_celulas/
│
├── cell_counter/
│   ├── __init__.py
│   ├── step00_io.py
│   ├── step01_field.py
│   ├── step02_grayscale.py
│   ├── step03_intensity.py
│   ├── step04_spatial_filter.py
│   ├── step05_frequency_filter.py
│   ├── step06_edges.py
│   ├── step07_thresholding.py
│   ├── step08_segmentation.py
│   ├── step09_counting.py
│   └── step10_pipeline.py
│
├── demos/
│   └── demo_count_cells.py
│
├── images/
│   ├── sample_01.jpg
│   ├── sample_02.jpg
│   └── sample_03.jpeg
│
├── outputs/
│
├── README.md
├── requirements.txt
└── pyproject.toml
```

## Instalación

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno virtual en Windows:

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Instalar el paquete en modo editable:

```bash
pip install -e .
```

## Uso del demo

Ejecutar desde la carpeta principal del proyecto:

```bash
python demos/demo_count_cells.py
```

El programa mostrará las imágenes disponibles dentro de la carpeta `images/`.

Después se escribe el nombre de la imagen a procesar. Por ejemplo:

```text
sample_01
```

También se puede escribir con extensión:

```text
sample_01.jpg
```

El sistema procesará una sola imagen, mostrará cada etapa del procesamiento y guardará las salidas automáticamente.

## Salidas generadas

Las imágenes procesadas se guardan en la carpeta `outputs/`, usando el mismo nombre de la imagen de entrada.

Ejemplo:

```text
outputs/sample_01/
```

Dentro de esa carpeta se generan imágenes como:

```text
00_original.png
01_mascara_campo.png
02_campo_recortado.png
03_escala_de_grises.png
04_estiramiento_lineal.png
05_filtro_promediador.png
06_pasa_bajas_fft.png
07_sobel.png
08_otsu_lab_a.png
09_segmentacion_por_regiones.png
10_leucocitos_detectados.png
11_conteo_hough.png
```

## Ejemplo de resultado

Para la imagen `sample_01`, se obtuvo:

| Imagen | Conteo manual | Conteo automático | Error absoluto | Error porcentual |
|---|---:|---:|---:|---:|
| sample_01 | 346 | 366 | 20 | 5.78 % |

La diferencia puede deberse a células muy cercanas entre sí, células parcialmente cortadas, variaciones de contraste o falsas detecciones.

## Descripción de módulos

### `step00_io.py`

Contiene funciones para cargar imágenes, crear carpetas y guardar resultados.

### `step01_field.py`

Detecta el campo circular del microscopio y elimina el fondo negro externo.

### `step02_grayscale.py`

Convierte la imagen a escala de grises.

### `step03_intensity.py`

Aplica estiramiento lineal de contraste usando la máscara del campo útil.

### `step04_spatial_filter.py`

Aplica un filtro espacial promediador implementado manualmente.

### `step05_frequency_filter.py`

Aplica un filtro pasa-bajas en frecuencia usando FFT.

### `step06_edges.py`

Implementa convolución manual y detección de bordes con Sobel.

### `step07_thresholding.py`

Implementa umbralización mediante Otsu manual.

### `step08_segmentation.py`

Realiza segmentación por regiones conectadas y detección de leucocitos en espacio LAB.

### `step09_counting.py`

Realiza el conteo final mediante Transformada de Hough.

### `step10_pipeline.py`

Une todas las etapas del procesamiento en una sola función principal: `procesar_imagen()`.

## Uso como librería

También se puede usar desde Python:

```python
from cell_counter import procesar_imagen

resultados = procesar_imagen(
    img_path="images/sample_01.jpg",
    output_dir="outputs/sample_01",
    guardar_pasos=True,
    mostrar_pasos=True
)

print(resultados)
```

La función devuelve un diccionario con los resultados principales:

```python
{
    "imagen": "images/sample_01.jpg",
    "umbral_otsu_lab_a": 142,
    "regiones_validas": 295,
    "leucocitos": 7,
    "eritrocitos_hough": 366,
    "output_dir": "outputs/sample_01"
}
```

Los valores pueden cambiar dependiendo de la imagen procesada.

## Limitaciones

El algoritmo puede presentar errores en casos como:

- Células muy pegadas entre sí.
- Células parcialmente cortadas en los bordes.
- Cambios fuertes de iluminación.
- Variaciones en la tinción.
- Artefactos morados o azulados que puedan confundirse con leucocitos.
- Imágenes tomadas con diferente aumento del microscopio.

## Dependencias

```text
opencv-python
numpy
matplotlib
```

## Autor
```text
Equipo Proyecto 1
Cristian Alejandro Esquivel Garcia 
Joel de Jesus Rodriguez
Joel Marino 
Jose Luis Blandran Garza
```