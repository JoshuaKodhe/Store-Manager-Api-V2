from app.api.v2.utils.db_connection import init_db


class Product:
    def __init__(self, name, category, price, quantity, description):
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.description = description
        self.db = init_db()

    def save(self):
        '''Method to save a product by appending it to existing
        products table'''
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO products (name,category,price,quantity,description) \
              VALUES(%s,%s,%s,%s,%s)",
            (self.name, self.category, self.price,
             self.quantity, self.description),)

        self.db.commit()
        self.db.close()
