FROM balenalib/raspberry-pi-debian-python:latest

WORKDIR /app

RUN install_packages apt-utils
RUN install_packages i2c-tools
RUN install_packages python3-smbus
RUN install_packages python3-can

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
CMD [ "python3", "./main.py"]
