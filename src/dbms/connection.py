import os

import psycopg2
from dotenv import load_dotenv, find_dotenv

try:
    # Initialized env variables
    load_dotenv(find_dotenv())

    # Connect to the database
    conn = psycopg2.connect(
        host=os.environ['POSTGRES_HOST'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        database=os.environ['POSTGRES_DB'],
        port=os.environ['POSTGRES_PORT'],
    )
except Exception as e:
    print(f'Error while connecting to the database: {e}')