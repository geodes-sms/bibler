FROM python:3.9.14-slim-bullseye


WORKDIR /app

COPY requirements-web.txt src/bibler/requirements-web.txt

RUN pip install -U -r src/bibler/requirements-web.txt

RUN python -m spacy download en_core_web_trf

COPY . /app

CMD ["python", "src/bibler/web.py"]
