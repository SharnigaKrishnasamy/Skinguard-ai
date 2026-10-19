"""SkinGuard AI - image classifier.
Usage: from model.predict import predict ; predict(PIL_image) -> dict
Needs model.pt and config.json in the same folder as this file."""
import os, json
import torch, torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image

_DIR = os.path.dirname(os.path.abspath(__file__))
_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_model = None
_cfg = None
_tf = None

def _load():
    global _model, _cfg, _tf
    if _model is not None:
        return
    with open(os.path.join(_DIR, "config.json")) as f:
        _cfg = json.load(f)
    m = models.efficientnet_b0(weights=None)
    m.classifier[1] = nn.Linear(m.classifier[1].in_features, len(_cfg["class_order"]))
    m.load_state_dict(torch.load(os.path.join(_DIR, "model.pt"), map_location=_DEVICE))
    _model = m.to(_DEVICE).eval()
    size = _cfg["image_size"]
    _tf = transforms.Compose([
        transforms.Resize((size, size)),
        transforms.ToTensor(),
        transforms.Normalize(_cfg["mean"], _cfg["std"]),
    ])

def predict(image):
    """image: PIL.Image (or a file path). Returns label, confidence, top3, uncertain."""
    _load()
    if isinstance(image, (str, os.PathLike)):
        image = Image.open(image)
    image = image.convert("RGB")
    x = _tf(image).unsqueeze(0).to(_DEVICE)
    with torch.no_grad():
        logits = _model(x).float()
        probs = F.softmax(logits / _cfg["temperature"], dim=1)[0].cpu()
    classes = _cfg["class_order"]
    vals, idx = torch.topk(probs, k=3)
    top3 = [(classes[i], round(float(v), 4)) for v, i in zip(vals.tolist(), idx.tolist())]
    conf = float(vals[0])
    return {
        "label": classes[int(idx[0])],
        "confidence": round(conf, 4),
        "top3": top3,
        "uncertain": bool(conf < _cfg["uncertainty_threshold"]),
    }
