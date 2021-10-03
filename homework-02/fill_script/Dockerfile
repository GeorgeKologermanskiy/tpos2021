FROM ubuntu:20.04
RUN apt-get update 1>/dev/null
RUN apt-get -y install --no-install-recommends python3 python3-pip libpq-dev openssl wget tar wait-for-it 1>/dev/null

RUN pip install psycopg2-binary

COPY main.py /fill_script/main.py