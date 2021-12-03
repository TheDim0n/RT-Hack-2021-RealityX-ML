FROM python:3.9.9-slim

RUN apt-get update -y && \
    apt install -y libgl1-mesa-glx -y && \
    apt-get install libglib2.0-0 -y

RUN pip install --upgrade pip

WORKDIR /src

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD uvicorn api.main:app --host 0.0.0.0
