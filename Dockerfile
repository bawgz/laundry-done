FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends --assume-yes python3-smbus

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD [ "python", "./main.py"]
