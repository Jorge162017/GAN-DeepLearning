# Puerto Prisma — Diseño generativo de personajes

Proyecto 2 de Deep Learning, Universidad del Valle, 2026. GAN entrenada por el equipo para producir retratos de personajes de una ciudad imaginaria de comerciantes, inventores y exploradores. La presentación PDF está pendiente.

## Código y ejecución

Los seis notebooks están en `notebooks/`, numerados en orden: preparación de datos, base DCGAN, experimento de pérdida, experimento de estabilización, candidatos y vecinos, exportación. Se ejecutan en Google Colab. Desde el segundo se usa GPU T4 y acceso a Drive. Los datos y artefactos de cada ejecución se guardan en `Mi unidad/PuertoPrisma`. No se incluyen los 10000 datos de entrenamiento en Git.

Las instrucciones se concentran en este README; las celdas Markdown de los notebooks contienen solo títulos. El notebook 05 pide elegir checkpoint y justificarlo: se eligió opción 5, `stability_lr_d`, época 15. En el notebook 06, usar `IDS = [3, 5, 7, 13, 16, 24, 40, 93, 120, 163]` para la selección final; la carpeta de Colab se llama `galeria_provisional`.

La preparación también puede ejecutarse localmente con `python3 scripts/prepare_data.py`. Descarga la copia pública de Cartoon Set 10k y comprueba su SHA256 antes de extraer. En Colab no reinstalar una versión CPU de PyTorch sobre el entorno CUDA.

## Regenerar la galería incluida

Los pesos, vectores y 10 PNG finales están en `results/galeria_final/`. No se necesita descargar el dataset para regenerar.

```bash
python3 -m pip install -r requirements.txt
python3 scripts/regenerate_gallery.py --device cpu --output /tmp/puerto_prisma_regenerated
```

Para reproducir la verificación CUDA usar `--device cuda` con PyTorch 2.11.0 y CUDA 13.0 en Tesla T4. Se usa el lote de ruido completo guardado y los batches originales de 32; cada personaje tiene además su vector en `galeria/vectores_z.pt`, siguiendo el orden de `galeria/ids.json`. El script compara los PNG nuevos contra los entregados y escribe `verification.json`. Cambiar hardware o versiones puede introducir diferencias numéricas: el resultado exacto se verificó en el entorno de Colab, no se garantiza en todas las plataformas.

## Experimentos y resultados

DCGAN RGB 64 × 64, ruido de 100 dimensiones, Adam (0.5, 0.999), batch 128, 30 épocas y semilla 2026. Base: BCE no saturante y lr G/D 0.0002. Pérdida: solo etiqueta real de D 0.9. Estabilización: solo lr D 0.0001. Mismos datos, inicialización y ruido fijo. Semilla del ruido fijo: 2027. Los resultados reales están en `results/runs/`, con configuración, versiones, historia, curvas y evolución.

Los resultados no muestran una mejora visual consistente por aumentar las épocas. Para la galería se eligió la época 15 del experimento de estabilización por calidad y variedad visuales. Se generaron 200 candidatos con semilla 7070 y se eligieron 10 (5 %), por rostros reconocibles, menos artefactos, variedad en varios rasgos y revisión visual de vecinos. ID128 fue sustituido por ID013 por diversidad. Se preservan el lote de ruido y los vectores exactos.

La búsqueda de vecinos usa ResNet18 con pesos ImageNet y distancia coseno en las 10000 imágenes reales. Se guardan las parejas y distancias en `results/galeria_final/`. Las características de fotos ImageNet no certifican originalidad en caricaturas. Persisten ruido, deformaciones y repetición de arquetipos. Una sola semilla limita la generalización de los experimentos.

## Versiones

Entrenamiento registrado: Python 3.13.15, PyTorch 2.11.0+cu130, NumPy 2.1.3, Pillow 11.3.0, CUDA 13.0, Tesla T4. Las versiones efectivas están en los `config.json`; la versión usada para vecinos consta en `seleccion.json`. Para entrenar y medir vecinos en Colab se usan sus paquetes preinstalados de PyTorch, torchvision y matplotlib. `requirements.txt` cubre regeneración y manejo de notebooks; no fija el entorno de entrenamiento completo.

## Datos y atribución

Google LLC, **Cartoon Set**; componentes artísticos de Shiraz Fuman. Datos bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [Fuente original](https://google.github.io/cartoonset/download.html). [Copia de descarga](https://huggingface.co/datasets/cgarciae/cartoonset/tree/1.0.0/data), utilizada por error 403 del almacenamiento original. Modificaciones: transparencia sobre blanco y reducción de RGBA 500 × 500 a RGB 64 × 64, sin recorte ni aumento. Dataset validado: 10000 imágenes y cero duplicados exactos después del procesamiento. Los vecinos incluidos son imágenes de ese dataset, no personajes generados por la GAN.

## Uso de asistentes de IA

Codex se utilizó para interpretar requisitos, buscar fuentes, planificar, programar y revisar los notebooks, preparar herramientas de reproducción y ayudar al análisis. El equipo debe comprender y verificar el código y sus conclusiones. Ninguna imagen de la galería procede de un generador externo.

## Entrega

Repositorio: https://github.com/Jorge162017/GAN-DeepLearning. Canvas requiere código fuente, galería y `presentacion.pdf` de máximo 12 diapositivas más anexos opcionales. Los pesos del generador están incluidos (aproximadamente 14 MB). No hace falta publicar el dataset ni todos los checkpoints. El PDF aún no está creado.

Verificación adicional local: CPU con PyTorch 2.13.0 regeneró 9 PNG exactamente y el ID024 con diferencia máxima de 1 nivel de intensidad. Evidencia: `results/galeria_final/evidencias/regeneracion_cpu.json`. En T4/PyTorch 2.11.0+cu130 los 10 fueron idénticos, según `regeneracion.json`.
