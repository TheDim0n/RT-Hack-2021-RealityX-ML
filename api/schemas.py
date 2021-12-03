from typing import List
from pydantic import BaseModel


class Prediction(BaseModel):
    overall: bool
    n_full: int
    n_all: int
    url: str


class Body(BaseModel):
    img_size: int
    conf: float
    urls: List[str]
