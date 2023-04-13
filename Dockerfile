# APT
FROM ubuntu:bionic AS prereqs

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ=Etc/UTC
ENV LC_ALL "C.UTF-8"
ENV LANG "C.UTF-8"

RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get update -y && \
    apt-get install -y \
        build-essential \
        iputils-ping \
        python3-pip \
        wget \
        git \
        vim \
        net-tools \
        curl \
        telnet \
        apt-utils

RUN python3 -m pip install pip --upgrade

# PIP
FROM prereqs AS pip
COPY ./requirements.txt /
RUN pip3 install -r requirements.txt --retries 30 --default-timeout=60

# BASE
FROM pip AS development
COPY . /srv/app
WORKDIR /srv/app
CMD gunicorn \
    --bind 0.0.0.0:80 \
    --workers 1 \
    --threads 1 \
    --worker-connections 128 \
    --proxy-protocol \
    --reload \
    --timeout 300 \
    --graceful-timeout 1 \
    --log-level debug \
    run:app
