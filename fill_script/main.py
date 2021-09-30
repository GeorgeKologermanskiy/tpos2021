#!/usr/bin/env python3

import csv
import psycopg2
from time import sleep

dbname = 'simple'
user = 'Qwerty'
dbhost = 'database'
password = 'Qwerty5432'

# connect to db
conn = None
while True:
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, host=dbhost, password=password)
        break
    except psycopg2.OperationalError as e:
        sleep(1)

# drop table
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS tbl;")
conn.commit()
cur.close()

# create table
cur = conn.cursor()
cur.execute("CREATE TABLE tbl (id serial PRIMARY KEY, text varchar, value integer);")
conn.commit()
cur.close()

# build SQL write request
with open('/csv_data/data.csv', 'r') as csvfile:
    for i, row in enumerate(csv.reader(csvfile)):
        text = row[0]
        value = row[1]
        # write rows into database
        cur = conn.cursor()
        cur.execute("INSERT INTO tbl(text, value) VALUES(%s, %s)", (text, value))
        conn.commit()
        cur.close()
# close conn
conn.commit()
conn.close()

# check data
conn = psycopg2.connect(dbname=dbname, user=user, host=dbhost, password=password)
cur = conn.cursor()
cur.execute("SELECT * FROM tbl;")
a = cur.fetchall()
print(a)
cur.close()
conn.close()
