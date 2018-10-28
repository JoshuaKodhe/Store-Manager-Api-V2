class Product:
    product_list = []

    def __init__(self, name, description, quantity, price, category):
        self.product_id = len(self.product_list)+1
        self.product_name = name
        self.product_description = description
        self.product_quantity = quantity
        self.unity_price = price
        self.category = category

    def save_product(self):
        product = dict(product_id=self.product_id,
                       product_name=self.product_name,
                       category=self.category,
                       product_description=self.product_description,
                       product_quantity=self.product_quantity,
                       unit_price=self.unity_price
                       )
        Product.product_list.append(product)
        return product

    def retrieve_products(self):
        return Product.product_list

    def retrieve_single_products(self, productId):
        for product_item in Product.product_list:
            if product_item['product_id'] == productId:
                return product_item
        return False

    def retrieve_single_products_by_name(self, productName):
        for product_item in Product.product_list:
            if product_item['product_name'] == productName:
                return product_item

    def update_product(self, name, category, description, quantity, price):
        product_item = Product.retrieve_single_products_by_name(self, name)
        if product_item['product_name'] == name:
            product_item["product_name"] = name
            product_item["category"] = category
            product_item["product_description"] = description
            product_item["product_quantity"] = quantity
            product_item["unit_price"] = price

            return product_item
