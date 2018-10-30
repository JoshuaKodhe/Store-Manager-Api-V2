import unittest
from flask import current_app
from app import create_app
from app.db_setup import DB


class BasicTestCase(unittest.TestCase):
    '''Set up method to create an attendant, admin, product,
    and a sales table for use in other tests and authentication'''

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.db = DB("testing")
        self.db.create_tables()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        '''Method to clear all tables
        before another test is undertaken'''
        self.db.destroy_tables()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
