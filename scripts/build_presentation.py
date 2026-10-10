"""Construye la presentación académica de 12 páginas con PyMuPDF."""
from pathlib import Path
import json
import fitz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"presentacion.pdf"
ASSETS=ROOT/"results/galeria_final"
RUNS=ROOT/"results/runs"
NAVY=(0.09,0.16,0.25); INK=(0.17,0.22,0.28); MUTED=(0.39,0.44,0.49)
TEAL=(0.0,0.43,0.45); LIGHT=(0.94,0.96,0.96); ORANGE=(0.80,0.40,0.17)
WHITE=(1,1,1)
doc=fitz.open()
hist={p.parent.name:json.loads(p.read_text()) for p in RUNS.glob("*/history.json")}
selection=json.loads((ASSETS/"seleccion.json").read_text())
ids=selection["ids"]

def text(page,box,s,size=15,bold=False,color=INK):
    result=page.insert_textbox(fitz.Rect(box),s,fontname="hebo" if bold else "helv",fontsize=size,color=color,lineheight=1.23)
    if result<0:raise RuntimeError(f"Texto desborda: {s[:80]} ({result})")

def page(title,kicker):
    p=doc.new_page(width=960,height=540)
    p.draw_rect(p.rect,color=None,fill=WHITE)
    p.draw_rect(fitz.Rect(36,32,42,62),color=None,fill=TEAL)
    text(p,(54,29,920,48),kicker.upper(),10,True,TEAL)
    text(p,(54,52,920,96),title,27,True,NAVY)
    p.draw_line((40,503),(920,503),color=(0.83,0.87,0.88),width=0.6)
    text(p,(40,512,820,533),"UVG  /  Deep Learning 2026  /  Puerto Prisma",9,color=MUTED)
    text(p,(870,511,922,533),f"{len(doc):02d} / 12",10,True,MUTED)
    return p

def image(p,path,box):p.insert_image(fitz.Rect(box),filename=str(path),keep_proportion=True)
def note(p,s,y=457):text(p,(40,y,920,498),s,11,color=MUTED)
def link(p,label,url,box):
    text(p,box,label,10,color=TEAL)
    p.insert_link({"kind":fitz.LINK_URI,"from":fitz.Rect(box),"uri":url})
def card(p,box,title,body):
    r=fitz.Rect(box);p.draw_rect(r,color=None,fill=LIGHT)
    text(p,(r.x0+16,r.y0+13,r.x1-16,r.y0+43),title,17,True,NAVY)
    text(p,(r.x0+16,r.y0+49,r.x1-16,r.y1-10),body,14)
def plot(p,box,rows,keys,title):
    r=fitz.Rect(box);text(p,(r.x0,r.y0,r.x1,r.y0+24),title,13,True)
    x0,y0,x1,y1=r.x0+36,r.y0+35,r.x1-8,r.y1-30
    ymax=max(max(row[k] for row in rows) for k,_ in keys)*1.08
    for j in range(5):
        yy=y1-(y1-y0)*j/4
        p.draw_line((x0,yy),(x1,yy),color=(0.87,0.90,0.91),width=.5)
        text(p,(r.x0,yy-6,x0-5,yy+12),f"{ymax*j/4:.1f}",9,color=MUTED)
    for idx,(key,label) in enumerate(keys):
        color=TEAL if idx==0 else ORANGE
        points=[fitz.Point(x0+(x1-x0)*(row["epoch"]-1)/29,y1-(y1-y0)*row[key]/ymax) for row in rows]
        shape=p.new_shape();shape.draw_polyline(points);shape.finish(color=color,width=1.7,closePath=False);shape.commit()
        text(p,(x0+idx*140,y1+9,x0+(idx+1)*140,y1+27),label,10,True,color)
    text(p,(x1-61,y1+9,x1+5,y1+27),"30 épocas",9,color=MUTED)

p=page("Puerto Prisma","Proyecto 2 · Diseño generativo de personajes")
text(p,(54,117,530,177),"Crear un universo que no existe",24,True,NAVY)
text(p,(54,192,515,278),"Generación de retratos con una DCGAN, experimentos controlados y evidencia de diversidad y similitud con los datos.",19)
text(p,(54,319,520,387),"Jorge López · 221038\nÁngel Herrarte · 22873",19,True)
text(p,(54,405,520,461),"Universidad del Valle de Guatemala\nDeep Learning 2026 · Docente: Kevin Recinos",13,color=MUTED)
image(p,ASSETS/"evidencias/galeria_provisional.png",(558,120,918,420))
link(p,"Código, pesos y evidencias en GitHub", "https://github.com/Jorge162017/GAN-DeepLearning",(558,440,918,463))

p=page("Un universo definido por sus retratos","01 · Universo y datos")
card(p,(40,118,470,323),"Puerto Prisma","Ciudad imaginaria de comerciantes, inventores y exploradores. Retratos para un videojuego narrativo: vista frontal, colores planos, fondo blanco y rasgos simplificados.\n\nCriterio visual: reconocer un rostro y variar cabello, forma facial y accesorios dentro de un estilo común.")
card(p,(490,118,920,323),"Cartoon Set 10k","10 000 caricaturas por composición de piezas, de Google LLC; arte de Shiraz Fuman.\n\nDatos: licencia CC BY 4.0. Sin fotos de personas reales. Originales RGBA 500 × 500; salida RGB 64 × 64 con transparencia sobre blanco y Lanczos. Sin recorte ni aumento.")
text(p,(40,341,920,395),"Validación: 10 000 imágenes decodificables; 0 duplicados exactos a 64 × 64. Se conserva el origen de cada imagen y el SHA256 del archivo descargado.",15)
link(p,"Fuente y licencia: Google Cartoon Set", "https://google.github.io/cartoonset/download.html",(40,415,440,437))
link(p,"Copia de descarga: cgarciae / Hugging Face", "https://huggingface.co/datasets/cgarciae/cartoonset/tree/1.0.0/data",(490,415,920,437))
note(p,"El almacenamiento original devolvió 403; se usó una copia con integridad comprobada. Los vecinos mostrados se atribuyen al dataset.")

p=page("DCGAN: una base simple y reproducible","02 · Arquitectura y entrenamiento")
card(p,(40,119,470,309),"Generador G","Ruido z: 100 × 1 × 1.\nConvTranspose: 512 -> 256 -> 128 -> 64 -> 3 canales.\nResoluciones: 4 -> 8 -> 16 -> 32 -> 64.\nBatchNorm + ReLU; salida Tanh en [-1, 1].")
card(p,(490,119,920,309),"Discriminador D","Imagen RGB 64 × 64.\nConv: 64 -> 128 -> 256 -> 512 -> 1 canal.\nLeakyReLU (0.2); BatchNorm en bloques internos.\nSalida: un logit, sin sigmoid en la pérdida.")
text(p,(40,331,920,405),"BCEWithLogitsLoss: D distingue reales y falsas; G usa la pérdida no saturante con objetivo real. Adam: betas (0.5, 0.999), batch 128 y lr base 0.0002.\n30 épocas por ejecución; Colab Tesla T4; checkpoint completo después de cada época.",16)
link(p,"Referencia de arquitectura: tutorial DCGAN de PyTorch", "https://docs.pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html",(40,424,920,446))
note(p,"Elegimos DCGAN por su implementación explicable y su costo manejable a 64 × 64; mayor resolución no era necesaria para el alcance.")

p=page("Tres ejecuciones; un cambio por experimento","03 · Diseño experimental")
rows=[("Base","BCE no saturante","lr G = lr D = 0.0002"),("Pérdida","Etiqueta real D: 1.0 -> 0.9","Falsa D = 0; objetivo G = 1"),("Estabilización","lr D: 0.0002 -> 0.0001","lr G conserva 0.0002")]
for i,(a,b,c) in enumerate(rows):
    y=123+i*77
    p.draw_rect(fitz.Rect(40,y,920,y+66),color=None,fill=LIGHT)
    text(p,(56,y+15,236,y+53),a,17,True)
    text(p,(245,y+16,579,y+52),b,15)
    text(p,(596,y+16,910,y+52),c,14)
text(p,(40,368,920,431),"Controles: mismo dataset, arquitectura, semilla 2026, inicialización, batch 128, 30 épocas y orden de batches. Ruido fijo: 16 vectores, semilla 2027.\nCada experimento parte desde cero y se compara con la base; no combinamos ambos cambios.",15)
note(p,"Hipótesis registradas antes de entrenar. Una sola semilla limita las conclusiones; las pérdidas con etiquetas distintas no son directamente equivalentes.")

p=page("Del ruido a rostros reconocibles","04 · Evidencia obligatoria: ruido fijo")
image(p,RUNS/"base_bce/fixed_evolution.png",(40,115,920,302))
plot(p,(40,318,440,452),hist["base_bce"],[("g_loss","G"),("d_loss","D")],"Pérdidas BCE · base")
text(p,(474,321,920,456),"Mismos 16 vectores: aparecen rostros hacia época 15. A la 30: G = 5.853, D = 0.234 y D(fake) = 0.071; D domina, no es señal de éxito.\nPersisten ruido y repetición de rasgos. No se ve colapso completo en esta rejilla; posible colapso parcial.",13)
note(p,"16 ejemplos no descartan memorización. El cuadro gris inicial corresponde al modelo sin entrenar. G y D no deben bajar juntas.",469)

p=page("Pérdida: suavizado de etiquetas reales","05 · Hipótesis y resultado")
text(p,(40,115,920,185),"Hipótesis previa: usar 0.9 en reales reduciría la confianza extrema de D y mejoraría calidad. Útil si la rejilla tiene menos artefactos y conserva rostros distintos, sin perder estructura.",15)
plot(p,(40,198,440,414),hist["loss_label_smoothing"],[("g_loss","G"),("d_loss","D")],"Pérdidas BCE · experimento 03")
image(p,RUNS/"loss_label_smoothing/fixed_evolution.png",(466,199,920,323))
text(p,(477,339,920,444),"Época 30: G = 4.774; D = 0.599.\nD(real) = 0.820; D(fake) = 0.079.\nMenor confianza sobre reales, compatible con la etiqueta 0.9. Mejora visual mixta; D sigue separando falsas.",13)
note(p,"Resultado: la hipótesis de mejora visual no queda confirmada. La pérdida de D cambia de objetivo; no interpretamos su magnitud como calidad.")

p=page("Estabilización: ralentizar las actualizaciones de D","06 · Hipótesis, resultado y elección")
text(p,(40,115,920,187),"Hipótesis previa: reducir lr D a 0.0001 daría a G oportunidad de aprender mejores rasgos. Útil si disminuyen artefactos y se mantiene diversidad, sin dominio persistente de D ni pérdida de discriminación.",15)
plot(p,(40,200,440,410),hist["stability_lr_d"],[("g_loss","G"),("d_loss","D")],"Pérdidas BCE · experimento 04")
image(p,RUNS/"stability_lr_d/fixed_evolution.png",(466,199,920,323))
text(p,(477,335,920,445),"Época 30: G = 3.884; D = 0.147.\nD(real) = 0.935; D(fake) = 0.064.\nD sigue dominando: no se resuelve el desequilibrio. Elegimos la época 15 por el equilibrio visual entre calidad y variedad.",13)
note(p,"La elección de época 15 es selección de checkpoint para la galería, no prueba de superioridad general. Más épocas no garantizaron mejor calidad.")

p=page("Diez habitantes de Puerto Prisma","07 · Galería final")
names=[("Ivo","Mensajero"),("Ada","Archivista"),("Nilo","Explorador"),("Lía","Cartógrafa"),("Vera","Mediadora"),("Teo","Inventor"),("Alma","Navegante"),("Bruno","Guardián"),("Sol","Aprendiz"),("Rui","Comerciante")]
for i,candidate_id in enumerate(ids):
    x=40+(i%5)*176;y=112+(i//5)*172
    image(p,ASSETS/"galeria"/f"personaje_{candidate_id:03d}.png",(x+20,y,x+148,y+128))
    name,role=names[i]
    text(p,(x+8,y+130,x+168,y+148),f"{name} · ID {candidate_id:03d}",11,True)
    text(p,(x+8,y+149,x+168,y+166),role,10,color=MUTED)
note(p,"Selección: 10 de 200 (5 %). Nombres y roles son autoría narrativa del equipo, no etiquetas predichas. PNG originales 64 × 64 sin retoques.")

p=page("Cada personaje frente a su vecino más cercano","08 · Evidencia obligatoria: similitud")
for i,row in enumerate(selection["neighbors"]):
    x=40+(i%5)*176;y=119+(i//5)*142;candidate_id=row["candidate_id"]
    image(p,ASSETS/"galeria"/f"personaje_{candidate_id:03d}.png",(x,y+18,x+78,y+96))
    image(p,ASSETS/"vecinos"/f"vecino_{candidate_id:03d}.png",(x+86,y+18,x+164,y+96))
    text(p,(x,y,x+172,y+17),f"ID {candidate_id:03d} · GAN / real",10,True)
    text(p,(x,y+101,x+172,y+124),f"d coseno = {row['cosine_distance']:.4f}",10,color=MUTED)
text(p,(40,413,920,457),"ResNet18 ImageNet, 512 características normalizadas; vecino de menor distancia coseno entre 10 000 imágenes. Se observan diferencias de cabello, contorno o accesorios; sin copias casi idénticas evidentes en estas parejas.",13)
note(p,"La medida no certifica originalidad. ImageNet difiere del dominio de caricaturas; varios personajes comparten vecino y requieren revisión visual.",469)

p=page("Selección honesta y reproducción comprobada","09 · Evidencia de proceso y entrega")
card(p,(40,120,470,333),"Selección: 10 / 200 = 5 %","Lote fijo: semilla 7070, 200 vectores guardados.\nCriterios: rostros reconocibles, menos artefactos, diferencias en varios rasgos y revisión de vecinos.\nID128 se sustituyó por ID013 por diversidad. La selección de checkpoint usó las rejillas fijas.")
card(p,(490,120,920,333),"Regeneración","Pesos de G, vectores exactos y batches originales de 32.\nT4 / PyTorch 2.11.0+cu130: 10 PNG idénticos; error máximo 0.\nCPU / PyTorch 2.13.0: 9 idénticos; ID024 con diferencia máxima de 1 nivel de intensidad.")
text(p,(40,351,920,409),"Repositorio: seis notebooks, script de regeneración, README, configuraciones, historias, curvas, galería, vecinos y pesos del generador. No requiere volver a entrenar para producir los 10 PNG.",15)
link(p,"github.com/Jorge162017/GAN-DeepLearning", "https://github.com/Jorge162017/GAN-DeepLearning",(40,422,920,446))
note(p,"Reproducción exacta comprobada en el entorno CUDA registrado; no se garantiza igualdad bit a bit al cambiar hardware o versiones.")

p=page("Lo aprendido y el caso más difícil de defender","10 · Conclusiones, límites y reflexión final")
card(p,(40,120,470,364),"Conclusiones y fallos","La GAN aprende estructura facial y estilo, pero conserva ruido, ojos deformados y contornos irregulares.\nD domina gran parte del entrenamiento. Los experimentos no confirman una mejora consistente; el lote repite arquetipos.\nLa selección visual mejora la galería, pero puede ocultar parte de los fallos si no se declara.")
card(p,(490,120,920,364),"Reflexión: personaje ID013","Es el caso más difícil de defender por compartir rostro frontal y cabello largo con su vecino, y por tener la menor distancia entre los 10: 0.2633.\nDifiere en color y configuración de rasgos, pero eso no basta por sí solo para afirmar novedad. Sugiere recombinación de patrones del universo, con originalidad limitada y verificable solo parcialmente.")
text(p,(40,389,920,443),"Límites: una sola semilla, evaluación visual, CNN de otro dominio y resolución 64 × 64. Siguiente mejora: repetir semillas y evaluar diversidad en todo el lote, antes de aumentar resolución.",14)
note(p,"Uso de IA declarado en README: planificación, programación y apoyo al análisis. Todas las imágenes finales provienen de la GAN entrenada por el equipo.")

p=page("Matriz de evidencias","11 · Guía de evaluación")
widths=[198,62,310,310];xs=[40,238,300,610,920]
headers=["Evidencia","Diap.","Conclusión","Limitación"]
y=117
p.draw_rect(fitz.Rect(40,y,920,y+34),color=None,fill=NAVY)
for i,h in enumerate(headers):text(p,(xs[i]+9,y+8,xs[i+1]-8,y+31),h,11,True,WHITE)
rows=[("Universo y datos","2","Estilo definido; 10 000 datos y licencia citados.","Retratos; sin cuerpo ni ambiente generado."),("Arquitectura y control","3-4","DCGAN explicable; un cambio por experimento.","Una semilla y presupuesto fijo."),("Ruido fijo","5","Del ruido a rostros; variedad visible.","16 ejemplos no descartan colapso parcial."),("Pérdida e hipótesis","6","Suavizado: menor confianza; mejora visual mixta.","Objetivos BCE distintos; no equivalencia directa."),("Estabilización y curvas","7","D sigue dominando; checkpoint 15 elegido.","Menor pérdida no prueba mayor calidad."),("Galería y selección","8, 10","10 PNG; selección 10/200 = 5 %.","Artefactos y repetición de arquetipos."),("Vecinos cercanos","9","Sin copias casi idénticas evidentes en parejas.","CNN ImageNet no certifica originalidad."),("Regeneración y reflexión","10-11","T4: error 0; ID013 es el caso más discutible.","Variación numérica fuera del entorno; novedad parcial.")]
for j,row in enumerate(rows):
    yy=151+j*39
    if j%2==0:p.draw_rect(fitz.Rect(40,yy,920,yy+39),color=None,fill=LIGHT)
    for i,value in enumerate(row):text(p,(xs[i]+9,yy+7,xs[i+1]-8,yy+38),value,10)
link(p,"Fuentes y código: README del repositorio", "https://github.com/Jorge162017/GAN-DeepLearning",(40,476,920,498))
doc.set_metadata(dict(title="Puerto Prisma — Proyecto 2 GAN",author="Jorge López 221038; Ángel Herrarte 22873",subject="Deep Learning 2026 · Universidad del Valle de Guatemala",keywords="GAN, DCGAN, Cartoon Set, reproducibilidad"))
assert len(doc)==12
doc.save(OUT,garbage=4,deflate=True)
print(f"PDF creado: {OUT} ({len(doc)} diapositivas)")
