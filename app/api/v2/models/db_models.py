import os
import psycopg2


class DB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            print("connected")
            self.cursor = self.conn.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_tables(self):
        tables = ["""
                  CREATE TABLE IF NOT EXISTS products(
                  id serial PRIMARY KEY,
                  name varchar(250) NOT NULL,
                  category varchar NOT NULL,
                  price float(45) NOT NULL,
                  quantity int NOT NULL,
                  description varchar(255) NOT NULL)
                  """,
                  ]

        for table in tables:
            self.cursor.execute(table)

        self.conn.commit()

    def destroy_tables(self):
        sql = [" DROP TABLE IF EXISTS products CASCADE",
               ]
        for string in sql:
            self.cursor.execute(string)
        self.conn.commit()
        self.conn.close()
