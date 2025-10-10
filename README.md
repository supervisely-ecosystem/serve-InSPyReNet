<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/115161827/228558305-dca13b94-a8c1-467e-883f-3a5c982cb91c.jpg"/>  

# Serve InSPyReNet

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Pretrained-Models">Pretrained Models</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Inference-Settings">Inference Settings</a> •
  <a href="#Related-apps">Related Apps</a> •
  <a href="#Acknowledgment">Acknowledgment</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](../../../../supervisely-ecosystem/serve-inspyrenet)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/serve-inspyrenet)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/serve-inspyrenet.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/serve-inspyrenet.png)](https://supervisely.com)

</div>

## Overview

This app deploys pretrained **InSPyReNet** model as a Supervisely Application for **Salient Instance Segmentation** tasks.

Models under a **Salient Instance Segmentation** task are usually used for separating foreground from background. They predict a mask for the foreground object. These models are **class-agnostic**, which means they can't predict a class label for an object.

The app allows you to apply the model to an image inside the **Supervisely platform** or beyond it (using the [Inference Session API](https://developer.supervisely.com/app-development/neural-network-integration/inference-api-tutorial)).

In our experience, **InSPyReNet** could give near perfect predictions, but it uses a lot of **CUDA memory** comparing to other models at this task.

## Pretrained models

The app can deploy pretrained model in two regimes:
- `Swin-B HD` with HD resolution (up to 1280 px in the longer image side). Good with large images, but may make empty or incorrect predictions for small images.
- `Swin-B 384x384`, which is inferred in constant 384x384 resolution and allocates less CUDA memory. Choose it if you have small images or you don't need to predict very small details in the image.

**Note:** `Swin-B HD` could require a GPU with large CUDA memory at inference (about 6 GB for an HD image).

**Trained on** a massive collection of datasets for Salient Object Detection: DUTS-TR, HRSOD-TR, UHRSD-TR, DIS-TR, DUTS-TE, DUT-OMRON, ECSSD,HKU-IS, PASCAL-S, DAVIS-S, HRSOD-TE,UHRSD-TE, FSS-1000, MSRA-10K, DIS-VD, DIS-TE1, DIS-TE2, DIS-TE3, DIS-TE4


### Prediction preview:
| Input    | Prediction   |
| -------- | ------------ |
| ![bird](https://user-images.githubusercontent.com/31512713/229130681-e5b12330-930b-4920-9a6c-0118453fcc63.jpg) | ![inspyrenet](https://user-images.githubusercontent.com/31512713/229130686-2710962a-7eac-4a6d-9c3b-f36db8ff4c9c.jpg) |


## How To Run

1. Start the application from Ecosystem
2. Open the app in your browser

<img src="https://user-images.githubusercontent.com/31512713/228279474-db869e95-f906-4ee6-b9f5-fe779a945dab.png" width="80%"/>

3. Select the model you want to deploy
4. Click **"SERVE"** button.
5. ✅ That's it! Now you can use other apps with your model.


## Inference Settings

- `bbox_padding`: (default `66%`) when applying the model to a crop of an image (ROI), this bbox_padding will expand the crop at the boundaries, getting more image context to the model (may lead to more accurate preditctions). The value can be measured either in pixels (e.g. `100px`) or in percentages (e.g. `10%`)
- `pixel_confidence_threshold`: (default `150`). The model predicts a "soft" masks, i.e. the mask values are in range 0-255, but the mask in Supervisely is a Bitmap and has only two values: 0-1 (one bit). With this threshold we will treat the pixels in the mask as **0** if they are below the **threshold** and as **1** if above.


## Related Apps

You can use deployed model in the following Supervisely Applications ⬇️ 

- [Apply Object Segmentor to Images Project](../../../../supervisely-ecosystem/apply-object-segmentor-to-images-project) - apply a salient segmentation model to labeled rectangles (bbox). A padding can be added to extend the boundaries.
    <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/apply-object-segmentor-to-images-project" src="https://user-images.githubusercontent.com/115161827/229510088-dfe8413f-ec09-4cca-988e-596aab4dd7d2.jpg" height="70px" margin-bottom="20px"/>

- [Apply NN to Images Project](../../../../../supervisely-ecosystem/nn-image-labeling/project-dataset) - app allows to play with different inference options and visualize predictions in real time.  Once you choose inference settings you can apply model to all images in your project to visually analyse predictions and perform automatic data pre-labeling. 
    <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/nn-image-labeling/project-dataset" src="https://i.imgur.com/M2Tp8lE.png" height="70px" margin-bottom="20px"/>  

- [Apply NN to Videos Project](../../../../supervisely-ecosystem/apply-nn-to-videos-project) - app allows to label your videos using served Supervisely models.  
  <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/apply-nn-to-videos-project" src="https://imgur.com/LDo8K1A.png" height="70px" margin-bottom="20px" />

- [NN Image Labeling](../../../../supervisely-ecosystem/supervisely-ecosystem%252Fnn-image-labeling%252Fannotation-tool) - integrate any deployed NN to Supervisely Image Labeling UI. Configure inference settings and model output classes. Press `Apply` button (or use hotkey) and detections with their confidences will immediately appear on the image.   
    <img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/nn-image-labeling/annotation-tool" src="https://i.imgur.com/hYEucNt.png" height="70px" margin-bottom="20px"/>



## Acknowledgment

- Based on: [https://github.com/plemeri/InSPyReNet](https://github.com/plemeri/InSPyReNet) ![GitHub Org's stars](https://img.shields.io/github/stars/plemeri/InSPyReNet?style=social). Code in this repository is distributed under the MIT license.
- Paper: [https://arxiv.org/abs/2209.09475](https://arxiv.org/abs/2209.09475)
