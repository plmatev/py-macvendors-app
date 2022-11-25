FROM python:3.9.6-slim-bullseye

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN apt-get update && apt-get install -y libcurl4-openssl-dev libssl-dev gcc

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./src .

ENV PYTHONPATH=$PWD

# ENTRYPOINT ["python3", "main.py"]
ENTRYPOINT ["gunicorn", "server.app:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--access-logfile", "-", "--bind", "0.0.0.0:8000"]
