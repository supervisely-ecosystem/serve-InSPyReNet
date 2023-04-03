import os, sys
import torch
from pathlib import Path
from PIL import Image, ImageOps

import supervisely as sly
from dotenv import load_dotenv
try:
    from typing import Literal
except ImportError:
    # for compatibility with python 3.7
    from typing_extensions import Literal
from typing import List, Any, Dict

from src import api
from src.model_zoo import model_zoo


load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))
root_source_path = str(Path(__file__).parents[1])

class InSPyReNet(sly.nn.inference.SalientObjectSegmentation):
    def load_on_device(
        self,
        model_dir: str = None,
        device: Literal["cpu", "cuda", "cuda:0", "cuda:1", "cuda:2", "cuda:3"] = "cpu",
    ):
        if self.gui:
            self.model_name = self.gui.get_checkpoint_info()["Model"]
        else:
            self.model_name = "SwinB HD"
            sly.logger.warn(f"GUI can't be used, default model is {self.model_name}.")
        
        model_info = model_zoo[self.model_name]
        self.device = device

        sly.logger.info(f"Downloading the model {self.model_name}...")
        weigths_path = os.path.join(model_dir, f"{self.model_name}.pth")
        res = api.download_weights(model_info["weights_url"], weigths_path)
        if not res:
            res = api.download_weights_alt(model_info["weights_url_alt"], weigths_path)
        assert res is not None, "Can't download model weigths"

        sly.logger.info(f"Building the model {self.model_name}...")
        self.model = api.build_model(self.model_name, weigths_path, self.device)

        self.class_names = ["object_mask"]
        print(f"✅ Model has been successfully loaded on {device.upper()} device")

    def predict(self, image_path: str, settings: Dict[str, Any]) -> List[sly.nn.PredictionMask]:
        threshold_default = self.custom_inference_settings_dict["pixel_confidence_threshold"]
        threshold = settings.get("pixel_confidence_threshold", threshold_default)
        img = Image.open(image_path).convert('RGB')
        img = ImageOps.exif_transpose(img)
        mask = self.model.process(img, type='map')  # RGB map
        mask = mask[...,0]
        mask = self.binarize_mask(mask, threshold)
        res = [sly.nn.PredictionMask(class_name=self.class_names[0], mask=mask)]
        return res
    
    def get_models(self):
        models = []
        for name, info in model_zoo.items():
            info = info.copy()
            info.pop("weights_url_alt")
            models.append({"Model": name, **info})
        return models

    def binarize_mask(self, mask, threshold):
        mask[mask < threshold] = 0
        mask[mask >= threshold] = 1
        return mask

    @property
    def model_meta(self):
        if self._model_meta is None:
            self._model_meta = sly.ProjectMeta(
                [sly.ObjClass(self.class_names[0], sly.Bitmap, [255, 0, 0])]
            )
            self._get_confidence_tag_meta()
        return self._model_meta

    def get_info(self):
        info = super().get_info()
        info["videos_support"] = True
        info["async_video_inference_support"] = True
        info["model_name"] = self.model_name
        return info

    def get_classes(self) -> List[str]:
        return self.class_names
    
    def support_custom_models(self):
        return False


m = InSPyReNet(
    use_gui=True,
    custom_inference_settings=os.path.join(root_source_path, "custom_settings.yaml"),
)

if sly.is_production():
    m.serve()
else:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device:", device)
    m.load_on_device(m.model_dir, device)
    image_path = "./demo_data/image_03.jpg"
    # rect = sly.Rectangle(360, 542, 474, 700).to_json()
    # ann = m._inference_image_path(image_path=image_path, settings={"rectangle": rect, "bbox_padding":"66%"}, data_to_return={})
    # ann.draw_pretty(sly.image.read(image_path), [255,0,0], 7, output_path="out.png")
    results = m.predict(image_path, settings={})
    vis_path = "./demo_data/image_03_prediction.jpg"
    m.visualize(results, image_path, vis_path, thickness=0)
    print(f"predictions and visualization have been saved: {vis_path}")
