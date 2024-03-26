import os

import psycopg2
# !!! psycopg2-binary is lib for postgreSQL. You need replace it with lib which fits with yours DBMS
from dotenv import load_dotenv, find_dotenv

try:
    # Initialized env variables
    load_dotenv(find_dotenv())

    # Connect to the database
    conn = psycopg2.connect(
        host=os.environ['DBMS_HOST'],
        user=os.environ['DBMS_USER'],
        password=os.environ['DBMS_PASSWORD'],
        database=os.environ['DBMS_DB'],
        port=os.environ['DBMS_PORT'],
    )
except Exception as e:
    print(f'Error while connecting to the database: {e}')
