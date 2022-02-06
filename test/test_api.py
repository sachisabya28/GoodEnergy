import os
import sys
import json
sys.path.append('../')
import unittest
import requests
from app import db
from app import models


class TestData(unittest.TestCase):
    def setUp(self):
        self.postal_code = 12345
        self.city = "Berlin"
        self.street = "Rheinsberger"
        self.house_number = "76/77"
        self.unit_price = 3.86
        self.grid_fees = 0.64
        self.kwh_price = 0.56

        # another location to test average
        self.postal_code2 = 12345
        self.city2 = "Berlin"
        self.street2 = "Rheinsberger"
        self.house_number2 = 76/77
        self.unit_price2 = 4.86
        self.grid_fees2 = 4.64
        self.kwh_price2 = 2.56
        self.yearly_kwh_consumption = 1000
        loc_data = models.Location(
            postal_code=self.postal_code,
            city=self.city,
            street=self.street,
            house_number=self.house_number,
            unit_price=self.unit_price,
            grid_fees=self.grid_fees,
            kwh_price=self.kwh_price
        )

        loc_data2 = models.Location(
            postal_code=self.postal_code2,
            city=self.city2,
            street=self.street2,
            house_number=self.house_number2,
            unit_price=self.unit_price2,
            grid_fees=self.grid_fees2,
            kwh_price=self.kwh_price2
        )
        db.session.add(loc_data)
        db.session.commit()
        db.session.add(loc_data2)
        db.session.commit()
        

    def tearDown(self):
        models.Location.query.filter_by(postal_code=self.postal_code).delete()
        db.session.commit()

    def _check_response_status(self, status_code, status):
        self.assertEqual(status_code, status)

    # positive test case    
    def testpricedata(self):
        url = 'http://127.0.0.1:8000/userdata'
        payload = {"postal_code": self.postal_code,
                   "city": self.city,
                   "street": self.street,
                   "house_number": self.house_number,
                   "yearly_kwh_consumption": self.yearly_kwh_consumption}
        resp = requests.post(url, json=payload)
        self._check_response_status(resp.status_code, requests.codes.ok)
        response = json.loads(resp.text)
    
        self.assertTrue('grid_fees' in response)
        self.assertTrue('kwh_price' in response)
        self.assertTrue('total_price' in response)
        self.assertTrue('unit_price' in response)

    # positive case to test with average price
    def testavgpricedata(self):
        url = 'http://127.0.0.1:8000/userdata'
        payload = {'postal_code': self.postal_code2,
                   'city': self.city2,
                   'street': self.street2,
                   'house_number': self.house_number2,
                   'yearly_kwh_consumption': self.yearly_kwh_consumption}
        
        avg_resp = requests.post(url, json=payload)
        self._check_response_status(avg_resp.status_code, requests.codes.ok)
        response = json.loads(avg_resp.text)
        
        self.assertTrue('grid_fees' in response)
        self.assertTrue('kwh_price' in response)
        self.assertTrue('total_price' in response)
        self.assertTrue('unit_price' in response)
    
    # negative test case
    def testinvaliddata(self):
        url = 'http://127.0.0.1:8000/userdata'
        payload = {'postal_code': self.postal_code,
                   'street': self.street,
                   'house_number': self.house_number,
                   'yearly_kwh_consumption': self.yearly_kwh_consumption}
        
        resp = requests.post(url, json=payload)
        response = json.loads(resp.text)
        self._check_response_status(response['statusCode'], 400)
        self.assertEqual(response['body'], "Bad JSON format")
        

if __name__ == '__main__':
    unittest.main()