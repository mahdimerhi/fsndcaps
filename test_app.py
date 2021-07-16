import os
import unittest
import json
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
from app import app, create_app
from database.models import db, setup_db, Drink


Manager_Token = {'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtlZGJsRHk2OHhSbWQ3WXhZaWhvcyJ9.eyJpc3MiOiJodHRwczovL3VkYWNhZmUuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwYzkwYmYwNmIxYWY5MDA2OGU2Y2UyOSIsImF1ZCI6WyJjb2ZmZWVzaG9wIiwiaHR0cHM6Ly91ZGFjYWZlLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MjYzNzE5MjYsImV4cCI6MTYyNjQ1ODMyNiwiYXpwIjoiVGdjaTduU3pPcGZndFRQaDlLYkVpbW9mdk9WWGF1RlAiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.s2fu7C6n3bTNq8ZDpXEFLV60CsCO5TdcnYGSRZb_2WEy7Db_BbS9uDU34PQ2Yq2cq4YKJV_ezEiLUh33ueR-8O2KlM_WT5DaTLJo6gCs3hOFR9xR2wr9qFMAVIo1av3FaiyI9VXv85K-jHPMX06XBb1C2QiyUEjW4xDuFVvdiyeOzaWqUrLgt0uh4uTq4t-6HH4mhfZtNI-efgE9PJhr-3klHDkJia6y5RKYeVaHM6iHxqgkIHs72aAz8TPTBJN0X7K2a9VhkiHZP6CYyjXKCkDJZYzNgXUYmom2d0lEuQwqJvdZ9X5Okw3M2mVPcBghMFEADFtB9Fok5-L7ielLpQ'}
Barista_Token = {'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtlZGJsRHk2OHhSbWQ3WXhZaWhvcyJ9.eyJpc3MiOiJodHRwczovL3VkYWNhZmUuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA0MzkxMDc0OTU3NTk4NjM3OTM0IiwiYXVkIjpbImNvZmZlZXNob3AiLCJodHRwczovL3VkYWNhZmUuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYyNjM3MTkxNywiZXhwIjoxNjI2NDU4MzE3LCJhenAiOiJUZ2NpN25Tek9wZmd0VFBoOUtiRWltb2Z2T1ZYYXVGUCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZHJpbmtzLWRldGFpbCJdfQ.IO6LpRmJ2g23KUReoNKI6WvAEUPYITQJXBofEFMNVJmBBjNiJiQLw6cFqM5Tr2RH7VpUFFbPn_F7A2FkNsEKCQ0-Bfwe0Y_mekLFZ145R9uM7adfFfGB-70zV3Gj84d4Fsq53pDZ2dld1XIPS48qjn_LWxBkbPqY6EMJCuC7mCyOm3nyeUOHGyV_vozq7FPkx5L8D27bEXxzX08H4y3q6tcFPtDxmv81suJ9lEDsVslyKLfk9r1Rgm8F_txT7QziuY_aCZOSOompCrQh5W4BgfCCPJg_RsVD3ltUn62vpf2aTSamyVCA_sjNbnkbo2OCp8KaHFmbM362DjPw7JJ3tw'}


class CoffeeShopTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def insert_data(self):
        drink1 = Drink(
            title='water',
            recipe='[{"name": "water", "color": "blue", "parts": 1}]'
        )
        drink2 = Drink(
            title='water2',
            recipe='[{"name": "water2", "color": "blue", "parts": 2}]'
        )
        drink3 = Drink(
            title='water3',
            recipe='[{"name": "water3", "color": "blue", "parts": 3}]'
        )
        drink4 = Drink(
            title='water4',
            recipe='[{"name": "water4", "color": "blue", "parts": 4}]'
        )
        drink5 = Drink(
            title='water5',
            recipe='[{"name": "water5", "color": "blue", "parts": 5}]'
        )

        drink1.insert()
        drink2.insert()
        drink3.insert()
        drink4.insert()
        drink5.insert()
        self.db.session.close()

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        database_path = os.environ.get('DATABASE_URL')
        setup_db(self.app, database_path=database_path)
        with self.app.app_context():
            self.db = db
            self.db.drop_all()
            self.db.create_all()
            self.insert_data()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Get drinks

    def test_get_drinks(self):
        res = self.client().get('/drinks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])

    # Update current drink by Barista
    def test_update_drink_by_barista(self):
        res = self.client().patch('/drinks/4', headers=Barista_Token,
                                  json={
                                      'title': 'Water123',  # title should be unique
                                      'recipe': {'color': 'blue', 'name': 'water', 'parts': 1}
                                  })

        data = json.loads(res.data)

        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test Barista get drinks detail
    def test_barista_get_drinks_detail(self):
        res = self.client().get('/drinks-detail', headers=Barista_Token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["drinks"])

    # Test patch drink does not exist

    def test_404_update_drink_does_not_exist(self):
        res = self.client().patch(
            '/drinks/999',
            headers=Manager_Token,
            json={
                "title": "Water",
                "recipe": {
                    "color": "blue",
                    "name": "water",
                    "parts": 2}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Test Barista has no access to delete drinks

    def test_delete_drink_by_barista(self):
        res = self.client().delete('/drinks/1', headers=Barista_Token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test_404_delete_drink_not_exist

    def test_404_delete_drink_not_exist(self):
        res = self.client().delete('/drinks/1000', headers=Manager_Token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Test failing to add a drink

    def test_404_fail_create_drink(self):
        res = self.client().post(
            '/drinks-post',
            headers=Manager_Token,
            json={
                'title': 'Water123',
                'recipe': {
                    'color': 'blue',
                    'name': 'water',
                    'parts': 1}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Test_403_delete_drink_unauthorized

    def test_403_delete_drink_unauthorized(self):
        res = self.client().delete('/drinks/1', headers=Barista_Token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['description'], 'Permission not found.')
        self.assertEqual(data['code'], 'unauthorized')

    # Test Barista cannot add drink

    def test_create_new_drink_by_barista(self):
        res = self.client().post('/drinks', headers=Barista_Token,
                                 json={
                                     "title": "new_drink1",  # title should be unique
                                     "recipe": {"color": "new_color", "name": "drink", "parts": 2}
                                 })

        data = json.loads(res.data)

        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test delete drink by Manager

    def test_delete_drink_by_manager(self):
        res = self.client().delete('/drinks/2', headers=Manager_Token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test add new drink by Manager

    def test_post_drink_by_manager(self):
        res = self.client().post('/drinks', headers=Manager_Token,
                                 json={
                                     "title": "American",
                                     "recipe": [{"color": "Black", "name": "American", "parts": 2}]
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Update current drink_by_manager

    def test_update_drink_by_manager(self):
        res = self.client().patch('/drinks/3', headers=Manager_Token,
                                  json={
                                      "title": "Water10",
                                      "recipe": [{"color": "blue", "name": "water", "parts": 10}]
                                  }
                                  )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable

if __name__ == "__main__":
    unittest.main()
