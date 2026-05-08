# Instrucciones de instalación

Este documento explica cómo instalar y ejecutar el proyecto **Proyecto 1 - Conteo automático de células en imágenes microscópicas**.

El proyecto puede instalarse de dos formas:

1. Clonando el repositorio completo desde GitHub.
2. Instalando directamente la librería con `pip`.

---

## 1. Requisitos previos

Antes de instalar el proyecto se recomienda tener instalado:

- Python 3.9 o superior.
- pip.
- Git, si se desea instalar directamente desde GitHub o clonar el repositorio.

Para verificar la versión de Python:

```bash
python --version
```

Para verificar que pip está instalado:

```bash
pip --version
```

Para verificar que Git está instalado:

```bash
git --version
```

Si el comando `git --version` no funciona, se debe instalar Git o usar la opción de descarga ZIP desde GitHub.

---

## 2. Opción recomendada: clonar el repositorio completo

Esta opción permite descargar el código, las imágenes de prueba y el demo.

```bash
git clone https://github.com/Alex-Eg2/proyecto-conteo-celulas.git
cd proyecto-conteo-celulas
```

---

## 3. Crear un entorno virtual

Se recomienda crear un entorno virtual para evitar conflictos con otras instalaciones de Python.

```bash
python -m venv .venv
```

### Activar entorno virtual en Windows

```bash
.venv\Scripts\activate
```

### Activar entorno virtual en Linux o macOS

```bash
source .venv/bin/activate
```

Después de activarlo, la terminal debería mostrar algo parecido a:

```text
(.venv)
```

---

## 4. Instalar dependencias

Con el entorno virtual activo, instalar las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

Las dependencias principales son:

```text
opencv-python
numpy
matplotlib
```

---

## 5. Instalar el paquete en modo editable

Desde la carpeta principal del proyecto, ejecutar:

```bash
pip install -e .
```

Esta instalación permite importar la librería `cell_counter` desde Python.

---

## 6. Ejecutar el demo

Para ejecutar el programa de demostración:

```bash
python demos/demo_count_cells.py
```

El programa mostrará las imágenes disponibles dentro de la carpeta `images/`.

Ejemplo:

```text
sample_01.jpg
sample_02.jpg
sample_03.jpeg
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

El programa procesará la imagen, mostrará cada etapa del algoritmo y guardará las salidas en la carpeta `outputs/`.

---

## 7. Verificar instalación

Para verificar que la librería se instaló correctamente, se puede abrir Python y ejecutar:

```python
from cell_counter import procesar_imagen

print("Paquete instalado correctamente")
```

También se puede probar con una imagen:

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

---

## 8. Instalación directa desde GitHub

También se puede instalar la librería directamente desde GitHub:

```bash
pip install git+https://github.com/Alex-Eg2/proyecto-conteo-celulas.git
```

Esta opción instala la librería, pero no es la mejor opción si se desea revisar fácilmente las carpetas `images/`, `demos/` y los archivos del repositorio.

Para usar la librería después de instalarla directamente:

```python
from cell_counter import procesar_imagen

resultados = procesar_imagen(
    img_path="ruta/a/imagen.jpg",
    output_dir="ruta/de/salida",
    guardar_pasos=True,
    mostrar_pasos=True
)

print(resultados)
```

Nota: para usar `pip install git+...` se necesita tener Git instalado y agregado al PATH del sistema.

---

## 9. Instalación sin Git

Si no se tiene Git instalado, se puede descargar el proyecto como archivo ZIP desde GitHub.

1. Entrar al repositorio:

```text
https://github.com/Alex-Eg2/proyecto-conteo-celulas
```

2. Presionar:

```text
Code → Download ZIP
```

3. Descomprimir el archivo.

4. Entrar a la carpeta descomprimida desde la terminal:

```bash
cd ruta/donde/se/descomprimio/proyecto-conteo-celulas
```

5. Instalar dependencias:

```bash
pip install -r requirements.txt
```

6. Instalar el paquete:

```bash
pip install -e .
```

7. Ejecutar el demo:

```bash
python demos/demo_count_cells.py
```

---

## 10. Uso en Spyder

Para usar el proyecto en Spyder, primero se debe instalar el paquete en el mismo entorno de Python que usa Spyder.

Desde Anaconda Prompt:

```bash
cd ruta/del/proyecto/proyecto-conteo-celulas
pip install -r requirements.txt
pip install -e .
```

Después abrir Spyder y probar:

```python
from cell_counter import procesar_imagen

resultados = procesar_imagen(
    img_path="images/sample_01.jpg",
    output_dir="outputs/sample_01_spyder",
    guardar_pasos=True,
    mostrar_pasos=True
)

print(resultados)
```

Si aparece el error:

```text
ModuleNotFoundError: No module named 'cell_counter'
```

significa que Spyder no está usando el mismo entorno donde se instaló el paquete.

Si aparece el error:

```text
ModuleNotFoundError: No module named 'cv2'
```

se debe instalar OpenCV:

```bash
pip install opencv-python
```

---

## 11. Problemas comunes

### Error: no se reconoce el comando git

Si aparece un error como:

```text
Cannot find command 'git'
```

significa que Git no está instalado o no está agregado al PATH.

Soluciones:

- Instalar Git desde:

```text
https://git-scm.com/download/win
```

- O descargar el proyecto como ZIP desde GitHub.

---

### Error: no se puede escribir en el entorno de conda

Si aparece un error como:

```text
EnvironmentNotWritableError
```

significa que el usuario no tiene permisos para modificar el entorno actual de conda.

Solución recomendada: crear un entorno nuevo.

```bash
conda create -n conteo_celulas python=3.11
conda activate conteo_celulas
```

Luego instalar el proyecto:

```bash
pip install -r requirements.txt
pip install -e .
```

---

### Error: no se encuentra la imagen

Si aparece un error relacionado con la imagen, revisar que el archivo exista dentro de la carpeta `images/`.

Ejemplo correcto:

```text
images/sample_01.jpg
```

Si se escribe el nombre en el demo, debe coincidir con el archivo real:

```text
sample_01
```

o:

```text
sample_01.jpg
```

---

## 12. Desinstalar el paquete

Si se desea desinstalar el paquete:

```bash
pip uninstall proyecto-conteo-celulas
```

---

## 13. Resumen rápido de instalación

Comandos principales:

```bash
git clone https://github.com/Alex-Eg2/proyecto-conteo-celulas.git
cd proyecto-conteo-celulas
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python demos/demo_count_cells.py
```
