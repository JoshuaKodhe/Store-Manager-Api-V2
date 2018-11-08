from app.utils.db_connection import connect


class Product:
    def __init__(self, name, category, price, quantity, description):
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.description = description

    def save(self):
        '''Method to save a product by appending it to existing
        products table'''
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO \
                    products (name,category,price,quantity,description)
                    VALUES(%s,%s,%s,%s,%s)\
                    RETURNING prod_id,name,category,price,
                    quantity, description""",
                    (self.name, self.category, self.price,
                     self.quantity, self.description))
                product = cursor.fetchone()
        return dict(name=product[1], category=product[2], price=product[3],
                    quantity=product[4], description=product[5])

    def retrieve_products(self):
        """Get all the products in the store"""
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM products;")
                products = cursor.fetchall()

                if not products:
                    return dict(products="No products live here currently")

            product_list = []

            for product in products:
                product_list.append(dict(id=product[0], name=product[1],
                                         category=product[2], price=product[3],
                                         quantity=product[4],
                                         description=product[5]))
            return product_list

    @classmethod
    def retrieve_product_by_id(cls, prod_id):
        """Method to fetch a single product by it's ID"""
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM products WHERE prod_id=%s;""",
                               (prod_id,))
                product = cursor.fetchone()

            if product:
                return dict(name=product[1], category=product[2],
                            price=product[3], quantity=product[4],
                            description=product[5])

    @classmethod
    def retrieve_product_by_name(cls, name):
        """Method to fetch a single product by it's ID"""
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM products WHERE name = %s""",
                               (name,))
                product = cursor.fetchone()
                if product:
                    return dict(prod_id=product[0], name=product[1],
                                category=product[2], price=product[3],
                                quantity=product[4], description=product[5])

    @classmethod
    def update_product(cls, name, category, price, quantity, description, prod_id):
        """Method to update a product"""
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE products SET name = %s, category = %s,
                     price = %s, quantity = %s, description = %s
                     WHERE prod_id = %s
                     RETURNING name,category,price, quantity, description""",
                    (name, category, price, quantity, description, prod_id))
                product = cursor.fetchone()
            return dict(name=product[0], category=product[1], price=product[2],
                        quantity=product[3], description=product[4])

    @classmethod
    def delete_product(self, prod_id):
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" DELETE FROM products WHERE prod_id = %s
                                RETURNING name""",
                               (prod_id,))
                delete_product = cursor.fetchone()
                return dict(name=delete_product[0])
