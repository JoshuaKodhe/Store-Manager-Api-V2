
import os
import psycopg2

from instance.config import APP_CONFIG

environment = os.environ["APP_SETTINGS"]
DATABASE_URL = APP_CONFIG[environment].DATABASE_URL


def connect():
    return psycopg2.connect(DATABASE_URL)
