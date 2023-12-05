import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']

SECRET_AUTH = os.environ['SECRET_AUTH']
LIFETIME_TOKEN = int(os.environ['LIFETIME_TOKEN'])