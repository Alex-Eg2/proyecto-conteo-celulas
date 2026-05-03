import os
import cv2
import numpy as np

from .step00_io import cargar_imagen, guardar_figura, guardar_comparacion, crear_carpeta
from .step01_field import detectar_campo, recortar_campo
from .step02_grayscale import convertir_grises
from .step03_intensity import estiramiento_lineal
from .step04_spatial_filter import filtro_promediador
from .step05_frequency_filter import filtro_pasa_bajas_fft
from .step06_edges import sobel
from .step07_thresholding import otsu_manual, limpiar_binaria
from .step08_segmentation import obtener_canales_lab, segmentar_regiones, detectar_leucocitos
from .step09_counting import conteo_hough


def procesar_imagen(img_path,
                    output_dir="outputs",
                    guardar_pasos=True,
                    mostrar_pasos=False,
                    dp=1.2,
                    min_dist=16,
                    param1=80,
                    param2=18,
                    min_rad=6,
                    max_rad=18):
    crear_carpeta(output_dir)

    # 1. Lectura
    img = cargar_imagen(img_path)

    if guardar_pasos:
        guardar_figura(0, "Original", img, output_dir, mostrar=mostrar_pasos)

    # 2. Campo del microscopio
    campo_bin = detectar_campo(img)

    if guardar_pasos:
        guardar_figura(1, "Mascara campo", campo_bin, output_dir, mostrar=mostrar_pasos)

    # 3. Recorte
    img_campo, mask_rec = recortar_campo(img, campo_bin)

    if guardar_pasos:
        guardar_figura(2, "Campo recortado", img_campo, output_dir, mostrar=mostrar_pasos)

    # 4. Escala de grises
    img_gris = convertir_grises(img_campo, mask_rec)

    if guardar_pasos:
        guardar_figura(3, "Escala de grises", img_gris, output_dir, mostrar=mostrar_pasos)

    # 5. Estiramiento lineal con máscara
    img_contraste = estiramiento_lineal(img_gris, mask_rec)

    if guardar_pasos:
        guardar_comparacion(
            "04_estiramiento_lineal.png",
            "Antes",
            img_gris,
            "Estiramiento lineal",
            img_contraste,
            output_dir,
            mostrar=mostrar_pasos
        )

    # 6. Filtrado espacial
    img_espacial = filtro_promediador(img_contraste, k=5)
    img_espacial = cv2.bitwise_and(img_espacial, img_espacial, mask=mask_rec)

    if guardar_pasos:
        guardar_comparacion(
            "05_filtro_promediador.png",
            "Antes",
            img_contraste,
            "Filtro promediador (k=5)",
            img_espacial,
            output_dir,
            mostrar=mostrar_pasos
        )

    # 7. Filtrado en frecuencia
    img_fft = filtro_pasa_bajas_fft(img_espacial, corte=90, mask=mask_rec)
    img_fft = cv2.bitwise_and(img_fft, img_fft, mask=mask_rec)

    if guardar_pasos:
        guardar_comparacion(
            "06_pasa_bajas_fft.png",
            "Antes",
            img_espacial,
            "Pasa-bajas FFT (corte=90)",
            img_fft,
            output_dir,
            mostrar=mostrar_pasos
        )

    # 8. Detección de bordes
    kernel_er = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mask_inner = cv2.erode(mask_rec, kernel_er, iterations=1)

    mag_sobel, bordes_sobel = sobel(img_fft, mask=mask_inner, ratio=0.08)

    if guardar_pasos:
        guardar_comparacion(
            "07_sobel.png",
            "Magnitud Sobel",
            mag_sobel,
            "Bordes Sobel",
            bordes_sobel,
            output_dir,
            mostrar=mostrar_pasos
        )

    # 9. Umbralización Otsu en canal A de LAB
    L, A, B = obtener_canales_lab(img_campo)

    a_masked = cv2.bitwise_and(A, A, mask=mask_rec)

    umbral, binaria = otsu_manual(a_masked, mask=mask_rec)

    blancos = np.sum(binaria == 255)
    negros = np.sum((binaria == 0) & (mask_rec > 0))

    if blancos > negros:
        binaria = cv2.bitwise_not(binaria)
        binaria = cv2.bitwise_and(binaria, binaria, mask=mask_rec)

    binaria = limpiar_binaria(binaria)

    if guardar_pasos:
        guardar_comparacion(
            "08_otsu_lab_a.png",
            "Canal A (LAB)",
            a_masked,
            f"Otsu manual t = {umbral}",
            binaria,
            output_dir,
            mostrar=mostrar_pasos
        )

    # 10. Segmentación por regiones
    regiones = segmentar_regiones(binaria, area_min=80, area_max=2500)

    img_reg = img_campo.copy()

    for reg in regiones:
        x, y, w, h = reg["bbox"]
        cx, cy = reg["centroide"]

        cv2.rectangle(img_reg, (x, y), (x+w, y+h), (255, 255, 0), 1)
        cv2.circle(img_reg, (cx, cy), 2, (255, 0, 0), -1)

    cv2.putText(
        img_reg,
        f"Regiones: {len(regiones)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    if guardar_pasos:
        guardar_figura(
            9,
            "Segmentacion por regiones",
            img_reg,
            output_dir,
            mostrar=mostrar_pasos
        )

    # 11. Detección de leucocitos
    mask_leuco, contornos_leuco = detectar_leucocitos(L, A, B, mask_rec)

    img_leuco = img_campo.copy()

    cv2.drawContours(img_leuco, contornos_leuco, -1, (255, 0, 255), 2)

    cv2.putText(
        img_leuco,
        f"Leucocitos: {len(contornos_leuco)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 255),
        2
    )

    if guardar_pasos:
        guardar_figura(
            10,
            "Leucocitos detectados",
            img_leuco,
            output_dir,
            mostrar=mostrar_pasos
        )

    # 12. Conteo final por Hough
    zona_busqueda = cv2.bitwise_and(mask_inner, cv2.bitwise_not(mask_leuco))

    detectados, img_clahe, suavizada = conteo_hough(
        img_gris,
        zona_busqueda,
        dp=dp,
        min_dist=min_dist,
        param1=param1,
        param2=param2,
        min_rad=min_rad,
        max_rad=max_rad
    )

    img_hough = img_campo.copy()

    cv2.drawContours(img_hough, contornos_leuco, -1, (255, 0, 255), 2)

    for x, y, r in detectados:
        cv2.circle(img_hough, (x, y), r, (0, 200, 0), 1)
        cv2.circle(img_hough, (x, y), 2, (0, 0, 255), -1)

    cv2.putText(
        img_hough,
        f"Conteo: {len(detectados)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 200, 0),
        2
    )

    if guardar_pasos:
        guardar_figura(
            11,
            "Conteo Hough",
            img_hough,
            output_dir,
            mostrar=mostrar_pasos
        )

    resultados = {
        "imagen": str(img_path),
        "umbral_otsu_lab_a": int(umbral),
        "regiones_validas": int(len(regiones)),
        "leucocitos": int(len(contornos_leuco)),
        "eritrocitos_hough": int(len(detectados)),
        "output_dir": str(output_dir)
    }

    return resultados