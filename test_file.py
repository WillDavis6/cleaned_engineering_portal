from app import app
from data_search_class import Test_class
from unittest import TestCase
from flask import session

class TestFlaskRoutes(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        

    def test_homepage(self):

        with self.client:
                
            #Simulate a post request
            response = self.client.get('/')

            #Check if response is successful (Status code 200)
            self.assertEqual(response.status_code, 400)

   
    
