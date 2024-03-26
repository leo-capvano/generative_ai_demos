import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
USER_PASSWORD = os.environ["USER_PASSWORD"]
DB_USER = os.environ["DB_USER"]
COLLECTION_NAME = os.environ["COLLECTION_NAME"]
TOP_K = int(os.environ["TOP_K"])

CONNECTION_STRING = f"postgresql+psycopg2://{DB_USER}:{USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
db_connection = psycopg2.connect(user=DB_USER,
                                 password=USER_PASSWORD,
                                 host=DB_HOST,
                                 port=DB_PORT,
                                 database=DB_NAME)
