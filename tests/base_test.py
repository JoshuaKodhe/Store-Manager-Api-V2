import unittest
from app import create_app
from app.v2.models.db_setup import DB


base_url = "/api/v2"


class BaseTest(unittest.TestCase):
    '''Set up method to create an attendant, admin, product,
    and a sales table for use in other tests and authentication'''

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.db = DB("testing")
        self.db.create_tables()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        '''Method to clear all tables
        before another test is undertaken'''
        self.db.destroy_tables()
        self.app_context.pop()
