import os
from tempfile import NamedTemporaryFile

from PIL import Image, ImageDraw

from .schema import Prediction
from .upload_file import upload_file

def draw_boxes(bboxes):
    preds = []
    for boxes in bboxes:
        img = boxes["image"]
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        img_w, img_h = img.size
        n_full = 0
        for box in boxes["bboxes"]:
            cls = box["class"]
            n_full += cls
            center_xy = box["center"]
            size = box["size"]
            lx = (center_xy[0]-size[0]/2)*img_w - 10
            rx = (center_xy[0]+size[0]/2)*img_w + 10
            ly = (center_xy[1]-size[1]/2)*img_h - 10
            ry = (center_xy[1]+size[1]/2)*img_h + 10
            color = "red" if cls == 1 else "green"
            draw.rectangle([lx, ly, rx, ry], outline=color, width=3)
        
        # with NamedTemporaryFile(mode="w", newline='', encoding="utf-8", suffix=".png") as f:
        img.save("tmp.png")
        url = upload_file("tmp.png", boxes["camera"], "last.png")
        preds.append(Prediction(
            overall=n_full/len(boxes["bboxes"]) > 0.5,
            n_full=n_full,
            n_all=len(boxes["bboxes"]),
            url=url
        ))
    os.remove("tmp.png")
    return preds