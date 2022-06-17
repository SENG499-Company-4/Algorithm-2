# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt
WORKDIR /app/TestExample

CMD ["python3", "./LinearRegTesting.py"]