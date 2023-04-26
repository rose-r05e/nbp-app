import unittest
import json
from server import app

class Testapp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_average_exchange_rate_weekday(self):
        response = self.app.get('/average_exchange_rate?currency_code=USD&date=2023-04-24')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data['average_exchange_rate'], (int, float))

    def test_average_exchange_rate_weekend(self):
        response = self.app.get('/average_exchange_rate?currency_code=USD&date=2023-04-22')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Weekend dates do not return data.')

    def test_max_min_average_valid_count(self):
        response = self.app.get('/max_min_average?currency_code=USD&count=5')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data['max_average'], (int, float))
        self.assertIsInstance(data['min_average'], (int, float))

    def test_max_min_average_invalid_count(self):
        response = self.app.get('/max_min_average?currency_code=USD&count=0')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Invalid count value. Please provide an integer between 1 and 255.')

    def test_major_difference_valid_count(self):
        response = self.app.get('/major_difference?currency_code=EUR&count=5')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data['major_difference'], (int, float))

    def test_major_difference_invalid_count(self):
        response = self.app.get('/major_difference?currency_code=EUR&count=0')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Invalid count value. Please provide an integer between 1 and 255.')

if __name__ == '__main__':
    unittest.main()
