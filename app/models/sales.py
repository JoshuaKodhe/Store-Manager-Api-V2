from app.utils.db_connection import connect


class Sales:
    def __init__(self, quantity, product_name, sale_attendant, total):
        self.name = product_name
        self.quantity = quantity
        self.sale_attendant = sale_attendant
        self.total = total

    def save_record(self):
        '''Method to save a product by appending it to existing
        sales table'''
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO
                    sales (quantity,product_name,sale_attendant,total)
                    VALUES(%s,%s,%s,%s) RETURNING sale_id,product_name,quantity,
                    sale_attendant,total""",
                    (self.quantity, self.name, self.sale_attendant,
                     self.total),)
                product = cursor.fetchone()
                return dict(name=product[1], quantity=product[2],
                            sale_attendant=product[3], sale_total=product[4])

    @classmethod
    def retrieve_sales(cls):
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM sales;")
                sales = cursor.fetchall()
                if not sales:
                    return dict(sales="No sales live here currently")

            sales_list = []
            for sale in sales:
                sales_list.append(dict(sale_attendant=sale[1],
                                       product=sale[2],
                                       quantity=sale[3]))
            return sales_list

    @classmethod
    def retrieve_sales_by_id(cls, sale_id):
        """Method to fetch a single product by it's ID"""
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM sales WHERE sale_id=%s""",
                               (sale_id,))
                sale = cursor.fetchone()
            if sale:
                return dict(sale_id=sale[0], sale_attendant=sale[1],
                            product=sale[2],
                            quantity=sale[3], price=sale[4])

    @classmethod
    def retrieve_sales_by_attendant(cls, sale_attendant):
        """Method to fetch a single product by it's ID"""
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM sales WHERE sale_attendant=%s""",
                               (sale_attendant,))
                sales = cursor.fetchall()
                if not sales:
                    return dict(sales="No sales live here currently")

            sales_list = []
            for sale in sales:
                sales_list.append(dict(sale_id=sale[0], sale_attendant=sale[1],
                                       product=sale[2], quantity=sale[3],
                                       price=sale[4]))
            return sales_list
