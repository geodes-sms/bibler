# FROM python:3.9-slim-bullseye

# RUN addgroup --gid 1001 bibler && \
#     adduser --disabled-password --gecos '' --uid 1001 --gid 1001 nonroot

# RUN apt update && \
#     apt install -y libexpat1-dev \
#     build-essential \
#     apache2 \
#     apache2-utils \
#     ssl-cert \
#     libapache2-mod-wsgi

# RUN pip install mod_wsgi-standalone spacy

# COPY apache.conf /etc/apache2/conf-available/mod-wsgi.conf
# ENV MOD_WSGI_USER=nonroot MOD_WSGI_GROUP=bibler

# WORKDIR /app

# COPY ./src /app

# CMD ["mod_wsgi-express", "start-server", "/app/webservice/application.py"]

# NEW DOCKERFILE

FROM debian:bullseye-slim

# RUN addgroup --gid 1001 bibler && \
#     adduser --disabled-password --gecos '' --uid 1001 --gid 1001 nonroot

RUN apt update && \
    apt install -y libexpat1-dev \
    build-essential \
    apache2 \
    apache2-utils \
    ssl-cert \
    libapache2-mod-wsgi-py3 \
    python3 \
    python3-pip

RUN pip install spacy

COPY apache.conf /etc/apache2/conf-available/mod-wsgi.conf
RUN a2enmod rewrite

WORKDIR /app
COPY ./src /app
COPY ./entrypoint.sh /usr/local/bin
RUN sed 's/\r$//g' /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
