# Fase 1: decisiones iniciales

Universo provisional: **Puerto Prisma**, ciudad imaginaria de comerciantes, inventores y exploradores. Retratos de caricatura para un videojuego narrativo: colores planos, contornos definidos, rasgos simplificados y variedad de cabello, forma facial y accesorios. Los datos no permiten prometer fondos o vestuario.

- Dataset: Google Cartoon Set 10k, 10000 retratos sintéticos por composición; no son fotos de personas reales.
- Fuente: https://google.github.io/cartoonset/download.html
- Atribución: Google LLC, Cartoon Set; componentes artísticos de Shiraz Fuman.
- Licencia de los datos: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
- Modificaciones previstas: fondo blanco para transparencia, resolución RGB 64 × 64, conservación de proporciones; sin recorte inicial ni aumento.
- Cómputo: Colab GPU; Mac M2 como alternativa. Rendimiento todavía no medido.
- Modelo: DCGAN implementada y entrenada; resultados en `results/runs/`.
- Semilla inicial: 2026.
- Criterios: rostro reconocible, estilo común, diversidad en varios rasgos y ausencia de copias casi idénticas según vecinos cercanos. La originalidad se evaluará al final, no se asume.

Datos preparados y tres entrenamientos completados; galería seleccionada y regeneración comprobada. Roles y nombres opcionales todavía pendientes.

Distribución: copia de cgarciae en Hugging Face (versión 1.0.0), pues el almacenamiento original devuelve 403. SHA256 esperado: 902145ad5096af10ca9ee200b648e2a60e8b6b83dd2f4dc5356817988be8ff43.

Preparación ejecutada: 10000 imágenes válidas, todas RGBA de 500 × 500; cero duplicados exactos en las versiones 64 × 64. Reporte y muestra en `reports/`.
