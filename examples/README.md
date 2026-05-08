# Ejemplos de uso

Esta carpeta contiene ejemplos para usar la librería de conteo automático de células.

## Ejemplo básico

```python
from cell_counter import procesar_imagen

resultados = procesar_imagen(
    img_path="images/sample_01.jpg",
    output_dir="outputs/sample_01",
    guardar_pasos=True,
    mostrar_pasos=True
)

print(resultados)
