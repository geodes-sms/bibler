FROM python:3.9.14-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && apt-get clean -y && rm -rf /var/lib/apt/lists/* 

COPY src/bibler/requirements-web.txt requirements-web.txt

RUN BLIS_ARCH="generic" pip install spacy --no-binary blis

RUN pip install -U -r requirements-web.txt

COPY src/bibler/ /app

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

CMD ["/bin/sh", "-c", "/app/entrypoint.sh"]
