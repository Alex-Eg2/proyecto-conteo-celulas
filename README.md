# Proyecto 1 - Conteo automático de células en imágenes microscópicas

Librería en Python para procesar imágenes microscópicas y realizar el conteo automático de células mediante técnicas de procesamiento digital de imágenes.

El sistema incluye preprocesamiento, filtrado, detección de bordes, umbralización, segmentación por regiones y conteo final mediante Transformada de Hough.

---

## Objetivo

Diseñar e implementar una librería en Python capaz de detectar, segmentar y contar células en imágenes microscópicas.

---

## Técnicas utilizadas

El proyecto integra:

- Conversión a escala de grises.
- Estiramiento lineal de contraste.
- Filtrado espacial.
- Filtrado en frecuencia mediante FFT.
- Detección de bordes con Sobel.
- Umbralización mediante Otsu.
- Segmentación por regiones conectadas.
- Detección de leucocitos.
- Conteo de eritrocitos mediante Transformada de Hough.

---

## Estructura del proyecto

```text
proyecto_conteo_celulas/
│
├── cell_counter/
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
├── images/
├── outputs/
├── README.md
├── INSTALL.md
├── EXAMPLES.md
├── requirements.txt
└── pyproject.toml
