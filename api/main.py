import requests

from fastapi import FastAPI, Depends
from io import BytesIO
from os.path import join
from PIL import Image
from tempfile import TemporaryDirectory, NamedTemporaryFile
from typing import List

from api import config

from .schema import Prediction
from .draw_boxes import draw_boxes
from yolov5.predict import run


settings = config.Settings()
app = FastAPI(redoc_url=None)




@app.post("/predict/")
async def predict(urls: List[str]):
    with TemporaryDirectory() as tmp_dir:
        for url in urls:
            camera = url.split('/')[-2]
            resp = requests.get(url)
            img = Image.open(BytesIO(resp.content))
            with NamedTemporaryFile(mode="w", delete=False, newline='', encoding="utf-8", dir=tmp_dir, suffix=f"_{camera}.png") as tmp_f:
                img.save(tmp_f.name)
                

        imgsz = (settings.img_size, settings.img_size)
        weights = settings.weights
        bboxes = run(weights=f"weights/{weights}.pt", source=tmp_dir, imgsz=imgsz)
        preds = draw_boxes(bboxes)
    return preds

    

