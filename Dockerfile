FROM python:3.9.14-slim-bullseye

RUN pip install -U -r requirements-web.txt

RUN python -m spacy download en_core_web_trf

WORKDIR /app

COPY . /app

CMD ["python", "src/bibler/web.py"]
