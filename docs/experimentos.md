# Experimentos controlados

## Base observada en Colab

El equipo completó 30 épocas en T4. Según las figuras compartidas, G baja aproximadamente de 15 a 5–6 con oscilaciones; D se mantiene mayormente por debajo de 0.6. D(real) ronda 0.9 y D(fake), medida antes de actualizar D, ronda 0.05–0.15. Esto sugiere dominio de D. La evaluación con los 16 vectores fijos pasa de ruido a rostros variados, aún con artefactos, contornos irregulares y rasgos deformados. No se ve colapso completo en esa pequeña rejilla; no puede descartarse colapso parcial ni memorización. El cuadro gris inicial corresponde a la muestra inicial del modelo, no prueba un fallo de carga.

La observación se basa en una captura, no en métricas leídas directamente de Drive. Los reportes numéricos y figuras originales ya se recibieron y están en `results/runs/`.

## Pérdida: etiquetas reales suavizadas

Solo cambia el objetivo real de D de 1.0 a 0.9. Objetivo falso 0.0 y objetivo de G 1.0. Misma BCE no saturante, red, inicialización y tasas. Notebook: `03_perdida_colab.ipynb`. Hipótesis escrita en el notebook y guardada antes del entrenamiento. Resultado visual preliminar: según la captura compartida del 03, G se estabiliza alrededor de 4.5; D(real) ronda 0.8–0.85, compatible con el objetivo real de 0.9. Mejora visual mixta; persisten artefactos. No demuestra mejora general.

## Estabilización: menor aprendizaje de D

Solo cambia lr de D de 0.0002 a 0.0001; G conserva 0.0002 y las etiquetas son las de la base. Notebook: `04_estabilizacion_colab.ipynb`. Hipótesis escrita en el notebook y guardada antes del entrenamiento. Resultado visual preliminar: según la captura compartida del 04, G ronda 3.5–4 y D(real) termina cerca de 0.95 con D(fake) cerca de 0.06. D sigue dominando. Algunos rostros parecen más limpios en época 15 que en 30; no se concluye mejora consistente.

## Controles y análisis

Cada experimento se compara con la base. Todos parten desde cero, con semilla 2026, misma arquitectura, 30 épocas, batch 128, mismos datos y mismo ruido fijo. No se combinan ambos cambios. Se evalúan calidad visual, diversidad aparente y curvas interpretadas. Las probabilidades de D no son métricas de calidad de imagen; las pérdidas con distintas etiquetas tampoco son directamente equivalentes. Una sola semilla limita las conclusiones. La prueba de vecinos cercanos se hará antes de elegir la galería.

## Cierre

Se eligió `stability_lr_d`, época 15, para producir 200 candidatos con semilla 7070. Selección final: 003, 005, 007, 013, 016, 024, 040, 093, 120, 163; 10/200 (5 %). Los vecinos y las distancias están documentados en `results/galeria_final/seleccion.json`. ID128 fue reemplazado por ID013 para aumentar variedad. Regeneración exacta en T4: error máximo 0; prueba CPU adicional: máximo 1 en ID024. La galería contiene artefactos y no se afirma originalidad absoluta.
