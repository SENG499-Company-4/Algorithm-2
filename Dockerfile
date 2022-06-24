# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

FROM python:3.9-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "app.py"]
