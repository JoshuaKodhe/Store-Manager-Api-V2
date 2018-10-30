import unittest
from flask import current_app

from .base_test import BaseTest


class BasicTestCase(BaseTest):
    '''Tsting that the app is running correctly'''

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
