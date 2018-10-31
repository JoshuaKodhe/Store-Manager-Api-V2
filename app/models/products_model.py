from app.utils.db_connection import init_db
import psycopg2.extras as extras


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
        cursor = self.db.cursor(cursor_factory=extras.DictCursor)
        cursor.execute(
            """INSERT INTO products (name,category,price,quantity,description)\
              VALUES(%s,%s,%s,%s,%s) RETURNING name, category,price,quantity,\
              description""",
            (self.name, self.category, self.price,
             self.quantity, self.description),)
        product = cursor.fetchone()

        self.db.commit()
        self.db.close()

        new_product = dict(name=product[0],
                           category=product[1],
                           price=product[2],
                           quantity=product[3])

        return new_product

    def retrieve_products(self):
        """Get all the products in the store"""
        cursor = self.db.cursor(cursor_factory=extras.DictCursor)
        cursor.execute("SELECT * FROM products WHERE name = %s;")
        products = cursor.fetchall()
        self.db.close()

        if not products:
            return dict(products="No products live here currently")

        product_list = []

        for row in products:
            product_list.append(dict(row))
        return product_list
