"""Descarga, valida y prepara Cartoon Set 10k. Python 3.10+."""
import argparse
import hashlib
import json
import random
import tarfile
import urllib.request
import urllib.error
from collections import Counter
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

URL = "https://huggingface.co/datasets/cgarciae/cartoonset/resolve/1.0.0/data/cartoonset10k.tgz"
EXPECTED_SHA256 = "902145ad5096af10ca9ee200b648e2a60e8b6b83dd2f4dc5356817988be8ff43"
SEED = 2026

def prepare(root):
    root = Path(root)
    data = root / "data"
    data.mkdir(parents=True, exist_ok=True)
    archive = data / "cartoonset10k.tgz"
    raw = data / "raw"
    processed = data / "processed" / "cartoonset64"
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    if not archive.exists():
        temporary = archive.with_suffix(".part")
        print("Descargando Cartoon Set 10k (~450 MB)...", flush=True)
        try:
            urllib.request.urlretrieve(URL, temporary)
        except (urllib.error.URLError, OSError) as exc:
            raise RuntimeError(
                f"No se pudo descargar {URL}. Descarga ese enlace y coloca "
                f"el archivo en {archive}. Error: {exc}"
            ) from exc
        temporary.rename(archive)
    digest = hashlib.sha256()
    with archive.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != EXPECTED_SHA256:
        raise RuntimeError("SHA256 inesperado: el archivo no coincide con la copia documentada.")
    raw.mkdir(exist_ok=True)
    if not (raw / ".extracted").exists():
        with tarfile.open(archive, "r:gz") as bundle:
            bundle.extractall(raw, filter="data")
        (raw / ".extracted").touch()
    files = sorted(raw.rglob("*.png"))
    if len(files) != 10000:
        raise RuntimeError(f"Se esperaban 10000 PNG; encontrados: {len(files)}")
    processed.mkdir(parents=True, exist_ok=True)
    sizes, modes, hashes = Counter(), Counter(), Counter()
    mapping = []
    for i, source in enumerate(files):
        with Image.open(source) as im:
            im.load()
            sizes[str(im.size)] += 1
            modes[im.mode] += 1
            rgba = im.convert("RGBA")
            background = Image.new("RGBA", rgba.size, "white")
            rgb = Image.alpha_composite(background, rgba).convert("RGB")
            # Preserva el rostro completo: sin recorte; padding si no es cuadrado.
            result = ImageOps.pad(rgb, (64, 64), method=Image.Resampling.LANCZOS, color="white")
            hashes[hashlib.sha256(result.tobytes()).hexdigest()] += 1
            target = processed / source.name
            result.save(target)
            mapping.append({"original": str(source.relative_to(root)), "prepared": str(target.relative_to(root))})
        if (i+1) % 1000 == 0:
            print(f"Preparadas {i+1}/10000", flush=True)
    selected = random.Random(SEED).sample(files, 36)
    sheet = Image.new("RGB", (6*144, 6*168), "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    for i, source in enumerate(selected):
        x, y = (i%6)*144, (i//6)*168
        with Image.open(processed / source.name) as im:
            sheet.paste(im.resize((128,128), Image.Resampling.NEAREST), (x+8,y+8))
        draw.text((x+8,y+140), str(i+1), fill="black")
    sheet.save(reports / "muestra_dataset.png")
    report = {"source": "https://google.github.io/cartoonset/download.html", "download_mirror": URL, "license": "CC BY 4.0", "count": len(files), "original_sizes": dict(sizes), "original_modes": dict(modes), "prepared_size": [64,64], "prepared_mode": "RGB", "duplicate_images_at_64": sum(n-1 for n in hashes.values()), "archive_sha256": digest.hexdigest(), "seed": SEED, "preprocessing": "White alpha composite, preserve aspect ratio, centered padding, Lanczos resize; no augmentation", "preview_files": [str(p.relative_to(root)) for p in selected]}
    (reports / "dataset_report.json").write_text(json.dumps(report, indent=2))
    (reports / "dataset_manifest.json").write_text(json.dumps(mapping, indent=2))
    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    prepare(parser.parse_args().root)
