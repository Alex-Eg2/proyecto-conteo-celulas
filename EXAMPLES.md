# Ejemplos de uso

Este documento muestra ejemplos para utilizar la librería **Proyecto 1 - Conteo automático de células en imágenes microscópicas**.

La librería permite procesar imágenes microscópicas, guardar imágenes intermedias y obtener un conteo automático de células mediante Transformada de Hough.

---

## 1. Ejecutar el demo incluido

Desde la carpeta principal del proyecto, ejecutar:

```bash
python demos/demo_count_cells.py
```

El programa mostrará las imágenes disponibles dentro de la carpeta `images/`.

Ejemplo:

```text
IMÁGENES DISPONIBLES EN LA CARPETA images/
--------------------------------------------------
- sample_01.jpg
- sample_02.jpg
- sample_03.jpeg
--------------------------------------------------
```

Después se debe escribir el nombre de la imagen a procesar.

Ejemplo sin extensión:

```text
sample_01
```

Ejemplo con extensión:

```text
sample_01.jpg
```

El programa procesará la imagen seleccionada, mostrará cada fase del algoritmo y guardará los resultados en la carpeta `outputs/`.

---

## 2. Salida esperada del demo

Al finalizar el procesamiento, la terminal mostrará un resumen parecido al siguiente:

```text
==================================================
RESULTADOS DEL PROCESAMIENTO
==================================================
Imagen procesada    : images/sample_01.jpg
Umbral Otsu LAB A   : 142
Regiones validas    : 295
Leucocitos          : 7
Eritrocitos Hough   : 366
Salidas guardadas   : outputs/sample_01
==================================================
```

Los valores pueden cambiar dependiendo de la imagen procesada.

---

## 3. Archivos generados

Para cada imagen procesada se crea una carpeta dentro de `outputs/` con el mismo nombre de la imagen.

Ejemplo:

```text
outputs/sample_01/
```

Dentro de esa carpeta se generan las imágenes intermedias:

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

Estas imágenes permiten revisar visualmente cada etapa del procesamiento.

---

## 4. Usar la librería desde Python

También se puede usar la librería directamente desde un archivo de Python.

Ejemplo:

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

Salida esperada:

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

---

## 5. Procesar una imagen nueva

Para procesar una imagen nueva, primero se debe colocar dentro de la carpeta `images/`.

Ejemplo:

```text
images/muestra_nueva.jpg
```

Luego se ejecuta el demo:

```bash
python demos/demo_count_cells.py
```

Cuando el programa pida el nombre de la imagen, escribir:

```text
muestra_nueva
```

También se puede escribir con extensión:

```text
muestra_nueva.jpg
```

La salida se guardará automáticamente en:

```text
outputs/muestra_nueva/
```

---

## 6. Procesar una imagen desde una ruta externa

Si la librería ya está instalada, también se puede procesar una imagen que esté fuera de la carpeta `images/`.

Ejemplo:

```python
from cell_counter import procesar_imagen

resultados = procesar_imagen(
    img_path=r"C:\Users\Usuario\Pictures\muestra.jpg",
    output_dir=r"C:\Users\Usuario\Pictures\salida_muestra",
    guardar_pasos=True,
    mostrar_pasos=True
)

print(resultados)
```

En este caso, las salidas se guardarán en:

```text
C:\Users\Usuario\Pictures\salida_muestra
```

---

## 7. Ejecutar sin mostrar ventanas

Si solo se desea guardar los resultados sin mostrar las imágenes durante la ejecución, usar:

```python
from cell_counter import procesar_imagen

resultados = procesar_imagen(
    img_path="images/sample_01.jpg",
    output_dir="outputs/sample_01_sin_ventanas",
    guardar_pasos=True,
    mostrar_pasos=False
)

print(resultados)
```

Esto es útil cuando se quiere procesar más rápido o evitar cerrar ventanas manualmente.

---

## 8. Ejecutar sin guardar imágenes intermedias

Si solo se desea obtener el resultado numérico:

```python
from cell_counter import procesar_imagen

resultados = procesar_imagen(
    img_path="images/sample_01.jpg",
    output_dir="outputs/sample_01",
    guardar_pasos=False,
    mostrar_pasos=False
)

print(resultados)
```

En este caso, el algoritmo procesa la imagen y devuelve el diccionario de resultados, pero no guarda todas las imágenes intermedias.

---

## 9. Cambiar parámetros de Hough

La etapa final usa Transformada de Hough para detectar estructuras aproximadamente circulares.

Los parámetros principales son:

| Parámetro | Descripción |
|---|---|
| `dp` | Resolución del acumulador de Hough |
| `min_dist` | Distancia mínima entre centros detectados |
| `param1` | Umbral alto usado internamente por Canny |
| `param2` | Sensibilidad de detección de círculos |
| `min_rad` | Radio mínimo esperado |
| `max_rad` | Radio máximo esperado |

Ejemplo:

```python
from cell_counter import procesar_imagen

resultados = procesar_imagen(
    img_path="images/sample_01.jpg",
    output_dir="outputs/sample_01_parametros",
    guardar_pasos=True,
    mostrar_pasos=True,
    dp=1.2,
    min_dist=16,
    param1=80,
    param2=18,
    min_rad=6,
    max_rad=18
)

print(resultados)
```

---

## 10. Ajustar el conteo automático

Si el algoritmo detecta demasiadas células, se puede intentar:

```python
param2=20
```

o aumentar la distancia mínima:

```python
min_dist=18
```

Ejemplo:

```python
from cell_counter import procesar_imagen

resultados = procesar_imagen(
    img_path="images/sample_01.jpg",
    output_dir="outputs/sample_01_ajustada",
    guardar_pasos=True,
    mostrar_pasos=True,
    param2=20,
    min_dist=18
)

print(resultados)
```

No se recomienda cambiar muchos parámetros al mismo tiempo, porque después es difícil saber cuál modificación afectó el resultado.

---

## 11. Resultados obtenidos con imágenes de prueba

Se probaron tres imágenes microscópicas incluidas en el proyecto.

| Imagen | Conteo automático Hough | Observación |
|---|---:|---|
| `sample_01` | 366 | Validada con conteo manual |
| `sample_02` | 426 | Conteo automático generado |
| `sample_03` | 442 | Conteo automático generado |

Para `sample_01`, se comparó el resultado con un conteo manual aproximado.

| Imagen | Conteo manual | Conteo automático | Error absoluto | Error porcentual |
|---|---:|---:|---:|---:|
| `sample_01` | 346 | 366 | 20 | 5.78 % |

El error porcentual se calculó como:

```text
Error % = |conteo automático - conteo manual| / conteo manual * 100
```

---

## 12. Interpretación de resultados

El conteo automático puede diferir del conteo manual por varias razones:

- Células muy cercanas entre sí.
- Células parcialmente cortadas en los bordes.
- Eritrocitos con bajo contraste.
- Variaciones en la iluminación.
- Artefactos de tinción.
- Leucocitos o zonas moradas cercanas a eritrocitos.
- Cambios en el tamaño aparente de las células.

Por esta razón, el conteo debe interpretarse como una estimación automática basada en procesamiento digital de imágenes.

---

## 13. Ejemplo mínimo

Este es el ejemplo más corto para usar la librería:

```python
from cell_counter import procesar_imagen

resultados = procesar_imagen("images/sample_01.jpg")

print(resultados["eritrocitos_hough"])
```

Este código procesa la imagen y muestra únicamente el conteo final de eritrocitos detectados.

---

## 14. Recomendación de uso

Para pruebas y revisión del proyecto se recomienda usar:

```bash
python demos/demo_count_cells.py
```

Para integrar la librería en otro programa se recomienda usar:

```python
from cell_counter import procesar_imagen
```
