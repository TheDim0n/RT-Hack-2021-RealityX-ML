import requests

from fastapi import FastAPI
from io import BytesIO
from os.path import join
from PIL import Image
from tempfile import TemporaryDirectory, NamedTemporaryFile
from typing import List

from .schemas import *
from .draw_boxes import draw_boxes
from yolov5.predict import run


app = FastAPI(redoc_url=None)


@app.post("/predict/{weights}/", response_model=List[Prediction])
async def predict(weights: str, data: Body):
    with TemporaryDirectory() as tmp_dir:
        for url in data.urls:
            camera = url.split('/')[-2]
            resp = requests.get(url)
            img = Image.open(BytesIO(resp.content))
            with NamedTemporaryFile(mode="w", delete=False, newline='', encoding="utf-8", dir=tmp_dir, suffix=f"_{camera}.png") as tmp_f:
                img.save(tmp_f.name)
                
        imgsz = (data.img_size, data.img_size)
        bboxes = run(weights=f"weights/{weights}.pt", source=tmp_dir, imgsz=imgsz, conf_thres=data.conf)
        preds = draw_boxes(bboxes, weights)
    return preds

    

