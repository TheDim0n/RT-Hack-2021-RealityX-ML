from pydantic import BaseModel


class Prediction(BaseModel):
    overall: bool
    n_full: int
    n_all: int
    url: str
