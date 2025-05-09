FROM python:3.9.14-slim-bullseye


WORKDIR /app

COPY src/bibler/requirements-web.txt src/bibler/requirements-web.txt

RUN if [ $TARGETARCH = "arm64" ]; then \
    apt-get update && apt-get install -y --no-install-recommends gcc build-essential && apt-get clean -y && rm -rf /var/lib/apt/lists/*  \
    BLIS_ARCH="generic" pip install --no-cache-dir --no-binary blis \
    ; fi
    
RUN pip install --no-cache-dir -U -r src/bibler/requirements-web.txt

RUN python -m spacy download en_core_web_trf

COPY . /app

CMD ["python", "src/bibler/web.py"]
