import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from database.models import setup_db, Employee, Department, Joining
from settings import TEST_DB_NAME, DB_PASSWORD, DB_USER, DB_CONN_STRING
from dotenv import load_dotenv

#database_path = os.environ['DATABASE_URL']
#if database_path.startswith("postgres://"):
#    database_path = database_path.replace("postgres://", "postgresql://", 1)
#database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_CONN_STRING, TEST_DB_NAME)

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(flag_db=False)
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_CONN_STRING, self.database_name)

        setup_db(self.app, self.database_path)

        self.token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdhT0tQQVVfWm15cThCZmFvMDlnUyJ9.eyJpc3MiOiJodHRwczovL2Rldi00NHJ0bWV2NHBwdGx5ZHV3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NWJmOTZjOThlOTlmZGU5Zjg2ZDQ4Y2IiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTcxMTU0NzI0NiwiZXhwIjoxNzExNTU0NDQ2LCJzY29wZSI6IiIsImF6cCI6InVSVGVBYXpyUW1kWFVjNzhUSkMzSVBLQzA2d2IzTzBtIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRlcGFydG1lbnQiLCJkZWxldGU6ZW1wbG95ZWUiLCJnZXQ6ZGVwYXJ0bWVudCIsImdldDplbXBsb3llZSIsImdldDpqb2luaW5nIiwicGF0Y2g6ZGVwYXJ0bWVudCIsInBhdGNoOmVtcGxveWVlIiwicG9zdDpkZXBhcnRtZW50IiwicG9zdDplbXBsb3llZSIsInBvc3Q6am9pbmluZyJdfQ.G8V3gZqpLIqvo7VIvAQpBZPwkMEigLIlpq-gPV8qoYm_Mi5QjImdJRmpbZcFVF3QEbmkMqHuJmwB-Bemu8f9j7XrguC1gwbfV_RvtYekI2ezDQPWtbSQlkuqGfWpKo7UeW0ryAuJ208N7dJTTJTWhQg04tPT1k4vUxFEojFl949wrACVSLhGL3wQS3j2X2ucYbiUXJAerV21Pe3MANpCYvFZ4H9IMpq5qxBtiG8qPw1j40Xm--r4x37IsZFwLGq7Z57-Y0MG9afWAvWY9ebL4_OeFxrybnb2iR2ExD2J-JzmA6EzRJQCJw_wfbszVTiscZYgmfkkSVt4g8tdHN8J1Q'

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
            }

        self.new_employee = {
            "name": "New Test Employee",
            "designation": "New Test Designation",
            "department_id": 105,
            "joining_date": "2018-10-11"
            }

        self.new_department = {
            "name": "New Test Department"
            }

        self.employee_id_del = 8

        self.department_id_del = 104

        self.updated_employee_data = {
            "name": "Update Test Employee",
            "designation": "Update Test Designation"
            }

        self.updated_department_data = {
            "name": "Update Test Department"
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
        self.assertEqual(response.status_code, 500)

    def test_get_employee_with_authentication(self):
        response = self.client().get('/employee', headers=self.headers)
        print(response)
        self.assertEqual(response.status_code, 200)
        print(response.data)

    def test_post_employee(self):
        response = self.client().post('/employee', json=self.new_employee, headers=self.headers)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_update_employee(self):
        employee_id = 2
        response = self.client().patch(f'/employee/{employee_id}', json=self.updated_employee_data, headers=self.headers)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_employee(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
            }
        response = self.client().delete(f'/employee/{self.employee_id_del}', headers=headers)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    # ----------------------------------------
    # Department
    # ----------------------------------------

    def test_get_department_without_authentication(self):
        response = self.client().get('/department')
        print(response)
        self.assertEqual(response.status_code, 500)

    def test_get_department_with_authentication(self):
        response = self.client().get('/department', headers=self.headers)
        print(response)
        self.assertEqual(response.status_code, 200)
        print(response.data)

    def test_post_department(self):
        response = self.client().post('/department', json=self.new_department, headers=self.headers)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_update_department(self):
        department_id = 105
        response = self.client().patch(f'/department/{department_id}', json=self.updated_department_data, headers=self.headers)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_department(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
            }
        response = self.client().delete(f'/department/{self.department_id_del}', headers=headers)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])


if __name__ == "__main__":
    unittest.main(exit=False)
