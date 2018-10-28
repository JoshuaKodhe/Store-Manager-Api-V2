import psycopg2


from app.api.v2.models.db_models import DB


class Product(DB):
    def __init__(self, name, category, price, quantity, description):
        super().__init__()
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.description = description

    def save(self):
        '''Method to save a product by appending it to existing
        products table'''
        self.create_tables()
        self.cursor.execute(
            "INSERT INTO products(name,category,price,quantity,description) VALUES(%s,%s,%s,%s,%s)",
            (self.name, self.category, self.price,
             self.quantity, self.description),
        )

        self.conn.commit()
        self.conn.close()
