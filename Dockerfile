FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN apt update && \
    apt install -y curl nano net-tools iputils-ping mc htop && \
    pip install --no-cache-dir --upgrade -r /app/requirements.txt && \
    ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

COPY . .

WORKDIR /app/src
