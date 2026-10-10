"""Regenera los 10 PNG usando pesos y vectores incluidos en el repositorio."""
import argparse
import json
from pathlib import Path
import torch
import numpy as np
from PIL import Image
from generator import Generator

def regenerate(assets, output, device):
    assets, output = Path(assets), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    state = torch.load(assets / "generator.pt", map_location="cpu", weights_only=True)
    z = torch.load(assets / "noise_pool.pt", map_location="cpu", weights_only=True)
    ids = json.loads((assets / "galeria/ids.json").read_text())
    model = Generator(state["config"]["latent_dim"], state["config"]["features"]).to(device).eval()
    model.load_state_dict(state["generator"])
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    errors = {}
    with torch.inference_mode():
        for start in sorted({((i-1)//32)*32 for i in ids}):
            batch = ((model(z[start:start+32].to(device)).cpu().clamp(-1,1)+1)*127.5).round().byte()
            for candidate_id in ids:
                index = candidate_id-1
                if start <= index < start+len(batch):
                    pixels = batch[index-start].permute(1,2,0).numpy()
                    name = f"personaje_{candidate_id:03d}.png"
                    Image.fromarray(pixels).save(output / name)
                    with Image.open(assets / "galeria" / name) as reference:
                        delta = np.abs(pixels.astype(np.int16)-np.asarray(reference.convert("RGB"),dtype=np.int16))
                    errors[str(candidate_id)] = int(delta.max())
    report = dict(device=str(device),torch_version=torch.__version__,max_pixel_errors=errors,
                  exact_match=all(v==0 for v in errors.values()))
    (output / "verification.json").write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets",default=str(Path(__file__).resolve().parents[1]/"results/galeria_final"))
    parser.add_argument("--output",default="regenerated_gallery")
    parser.add_argument("--device",choices=["cpu","cuda","mps"],default="cpu")
    args = parser.parse_args()
    regenerate(args.assets,args.output,torch.device(args.device))
