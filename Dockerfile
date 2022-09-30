FROM python:3.9.14-slim-bullseye

RUN pip install -U spacy fastapi uvicorn[standard]

RUN python -m spacy download en_core_web_trf

WORKDIR /app

COPY . /app

CMD ["python", "src/bibler/app.py"]
