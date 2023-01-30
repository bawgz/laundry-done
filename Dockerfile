FROM python:3.9-bullseye

WORKDIR /app

RUN apt update && apt install --no-install-recommends --assume-yes python3-smbus postgresql

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
CMD [ "python3", "./main.py"]
