FROM python:3.9.6-slim-bullseye

RUN mkdir -p /script && mkdir script/logs && mkdir script/input_data
WORKDIR /script

COPY requirements.txt ./requirements.txt

RUN apt-get update && apt-get install -y cron

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./src .

RUN echo '00  04  *  *  06  /usr/local/bin/python3 /script/main.py' > /etc/crontab
RUN cat /etc/crontab | crontab -

ENTRYPOINT ["cron", "-f"]