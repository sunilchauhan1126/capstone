import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import TEST_DB_NAME, DB_PASSWORD, DB_USER, DB_CONN_STRING
from dotenv import load_dotenv

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(flag_db=False)
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_CONN_STRING, self.database_name)

        setup_db(self.app, self.database_path)

        self.token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNub24zeFAwRE1NTERxdzd0cEppNSJ9.eyJpc3MiOiJodHRwczovL2thdnlhc3Jpay51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjVmYzYyYmQ4OWVlYmM0YjgyZjJkNTQzIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTcxMTM5MjYyNCwiZXhwIjoxNzExMzk5ODI0LCJzY29wZSI6IiIsImF6cCI6IlF3d0xTVDlCckQ3Vm9leWhNNzczbDJzVDdvMXY0TGpnIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.YR7-B5yv13teYFdugb2wG6l4vS6v1Ni8V-jw1HVsKATT6Rgg9Tu-GoWsafZzb3xKk-KfQ4KYeUFKDWh7rgiyayTOB7TwMnbYd415QsmEO8Fexi2jFffU22nYHNlKsUy_C11bBwSPtfpCZ8FtkYYZUCte6PLf9AuRhSQGjQDrzLse8_19jI0wDqM9Nrpv9mTwDcSRzKxLfIPpV3f4aY_G_9PjhxU7PlS8nAC0kKxdksgWvxfj8u0SLytzZypyXPbUqANE-fzgKXqPvR11LRyygsk4wga2sSEDBWwWLT6NBlaH2riUf_CERQuJk9T3OjZ0g2GKZhqloYmC8Ghepxx1_A'

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }

        self.new_employee = {
            "name": "New Test Employee",
            "designation": New Test Designation"
        }

        self.new_department = {
            "name": "New Test Department",
        }

        self.employee_id_del = 4

        self.department_id_del = 4

        self.updated_employee_data = {
            "name": "Update Test Employee",
            "designation": "Update Test Designation"
        }

        self.updated_department_data = {
            "name": "Update Test Department",
        }

    def tearDown(self):
        # with self.app.app_context():
        #     db.drop_all()
        pass

    # ----------------------------------------
    # Employee
    # ----------------------------------------

    def test_get_employee_without_authentication(self):
        response = self.client().get('/employee')
        print(response)

        self.assertEqual(response.status_code, 401)

    def test_get_employee_with_authentication(self):
        response = self.client().get('/employee', headers=self.headers)
        print(response)

        self.assertEqual(response.status_code, 200)
        print(response.data)

    def test_post_employee_with_authentication(self):
        response = self.client().post(
            '/employee', json=self.new_employee, headers=self.headers)
        print(response)

        self.assertEqual(response.status_code, 201)

    def test_update_employee(self):
        employee_id = 2
        response = self.client().patch(
            f'/employee/{employee_id}', json=self.updated_employee_data, headers=self.headers)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])

    def test_delete_employee(self):

        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        response = self.client().delete(
            f'/employee/{self.employee_id_del}', headers=headers)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])

    # ----------------------------------------
    # Department
    # ----------------------------------------

    def test_get_department_without_authentication(self):
        response = self.client().get('/department')
        print(response)

        self.assertEqual(response.status_code, 401)

    def test_get_department_with_authentication(self):
        response = self.client().get('/department', headers=self.headers)
        print(response)

        self.assertEqual(response.status_code, 200)
        print(response.data)

    def test_post_department_with_authentication(self):

        response = self.client().post(
            '/department', json=self.new_department, headers=self.headers)
        print(response)

        self.assertEqual(response.status_code, 201)

    def test_update_department(self):
        department_id = 6
        response = self.client().patch(
            f'/department/{departmentr_id}', json=self.updated_department_data, headers=self.headers)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])

    def test_delete_department(self):

        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        response = self.client().delete(
            f'/department/{self.department_id_del}', headers=headers)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])


if __name__ == "__main__":
    unittest.main(exit=False)
