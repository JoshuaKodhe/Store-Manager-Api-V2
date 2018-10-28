""" Sale Rcord Models """


class SaleRecordModel:
    """ Class the defines how our Sale records will look """
    sales_list = []

    def __init__(self, sold_by, name, unit_price, quantity, category):
        self.sale_id = len(self.sales_list)+1
        self.sale_attendant = sold_by
        self.product_name = name
        self.unit_price = unit_price
        self.quantity_sold = quantity
        self.category = category

    def save_record(self):
        """Method to save a sale record"""
        sale_record = dict(sale_id=self.sale_id,
                           sale_attendant=self.sale_attendant,
                           unit_price=self.unit_price,
                           product_name=self.product_name,
                           quantity_sold=self.quantity_sold,
                           category=self.category,
                           total_price=(self.quantity_sold*self.unit_price)
                           )
        SaleRecordModel.sales_list.append(sale_record)
        return sale_record

    def retrieve_records(self):
        """ Method to get all  sale records"""
        return SaleRecordModel.sales_list

    def retrieve_single_records(self, saleId):
        """ Method to get one sale record by the sale_record_id"""
        for product_item in SaleRecordModel.sales_list:
            if product_item['sale_id'] == saleId:
                return product_item
