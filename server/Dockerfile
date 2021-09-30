FROM ubuntu:20.04
RUN apt-get update 1>/dev/null
RUN apt-get -y install --no-install-recommends python3 python3-pip libpq-dev wait-for-it wget tar 1>/dev/null

RUN pip install psycopg2-binary bottle

COPY main.py /server/main.py