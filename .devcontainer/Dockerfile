# [Choice] Python version: 3, 3.8, 3.7, 3.6
FROM python:3.11.0-bullseye

RUN apt update
RUN apt install -y git \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1

RUN apt -f install -y
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y

RUN pip install selenium
RUN pip install webdriver-manager