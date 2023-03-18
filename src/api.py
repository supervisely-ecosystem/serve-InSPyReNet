import os
import gdown

from transparent_background import Remover
from src.model_zoo import model_zoo


def build_model(model_name, weights_path, device):
    fast = model_name == "SwinB low-res"
    return Remover(fast=fast, device=device, ckpt=weights_path)

def download_weights(url, output):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    if not os.path.exists(output):
        res = gdown.download(url, output=output)
        if not res:
            print("Google Drive has denied the download, trying slow method...")
            id = url.split("id=")[1]
            res = gdown.download(id=id, output=output, speed=5*1024*1024, use_cookies=False)
        return res
    else:
        return output

def download_weights_alt(url, output):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    if not os.path.exists(output):
        import onedrivedownloader
        res = onedrivedownloader.download(url, output)
        return res
    else:
        return output

