"""Database setup"""
import psycopg2

from instance.config import APP_CONFIG


class DB:
    """class that will be used for db operations"""
    def __init__(self, config_name):
        self.conn = psycopg2.connect(APP_CONFIG[config_name].DATABASE_URL)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Used for creating the tables"""
        tables = ("""
                  CREATE TABLE IF NOT EXISTS users(
                  user_id serial PRIMARY KEY,
                  email varchar(90) UNIQUE NOT NULL,
                  password varchar(120) NOT NULL,
                  registered_on varchar(100) NOT NULL)
                  """,

                  """
                  CREATE TABLE IF NOT EXISTS products(
                  prod_id serial PRIMARY KEY,
                  name varchar(100) UNIQUE NOT NULL,
                  category varchar(50) NOT NULL,
                  price float(45) NOT NULL,
                  quantity int NOT NULL,
                  description varchar(255) NOT NULL
                  )
                  """
                  )

        for table in tables:
            self.cursor.execute(table)

        self.conn.commit()

    def destroy_tables(self):
        """Used to remove tables from database"""
        sql = [" DROP TABLE IF EXISTS products CASCADE",
               " DROP TABLE IF EXISTS users CASCADE"
               ]
        for string in sql:
            self.cursor.execute(string)
        self.conn.commit()
        self.conn.close()
