FROM supervisely/base-py-sdk:6.73.418

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y build-essential
RUN apt-get install -y git ffmpeg libsm6 libxext6 ninja-build

RUN pip3 install torch==1.8.2 torchvision==0.9.2 --extra-index-url https://download.pytorch.org/whl/lts/1.8/cu111
RUN pip3 install timm gdown

RUN pip3 install onedrivedownloader \
    transparent-background==1.2.4 \
    kornia==0.5.11 \
    Pillow==9.2.0

RUN pip3 install supervisely==6.73.486

LABEL python_sdk_version="6.73.486"