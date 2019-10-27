FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential git python3.6 python3.6-dev python3-pip python3.6-venv bash vim
RUN python3.6 -m pip install pip --upgrade

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD python3.6 main.py