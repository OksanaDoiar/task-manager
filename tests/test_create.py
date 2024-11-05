import unittest
from flask import json

from app import app, task_manager, STATUS_CREATED, STATUS_BAD_REQUEST


class CreateTaskTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client for Flask
        self.app = app.test_client()
        self.app.testing = True

        # Clear existing tasks for a clean test environment
        task_manager.clear_all_tasks()  # Assuming `clear_all_tasks()` is a method to reset tasks for testing

    def test_create_task_success(self):
        # Data to be sent in the POST request
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "pending"
        }

        # Call the endpoint
        response = self.app.post('/tasks', data=json.dumps(task_data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, STATUS_CREATED)
        response_data = response.get_json()
        self.assertIn("id", response_data)

        # Check if the task is actually added in task_manager
        created_task = task_manager.get_task_by_id(response_data["id"])
        self.assertIsNotNone(created_task)
        self.assertEqual(created_task.title, "Test Task")
        self.assertEqual(created_task.description, "This is a test task")
        self.assertEqual(created_task.status, "pending")

    def test_create_task_missing_title(self):
        # Missing 'title'
        task_data = {
            "description": "This is a test task",
            "status": "pending"
        }

        # Call the endpoint
        response = self.app.post('/tasks', data=json.dumps(task_data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, STATUS_BAD_REQUEST)
        self.assertEqual(response.get_json(), {"error": "No title provided"})

    def test_create_task_missing_description(self):
        # Missing 'description'
        task_data = {
            "title": "Test Task",
            "status": "pending"
        }

        # Call the endpoint
        response = self.app.post('/tasks', data=json.dumps(task_data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, STATUS_BAD_REQUEST)
        self.assertEqual(response.get_json(), {"error": "No description provided"})

    def test_create_task_missing_status(self):
        # Missing 'status'
        task_data = {
            "title": "Test Task",
            "description": "This is a test task"
        }

        # Call the endpoint
        response = self.app.post('/tasks', data=json.dumps(task_data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, STATUS_BAD_REQUEST)
        self.assertEqual(response.get_json(), {"error": "No status provided"})

    def tearDown(self):
        # Clear tasks after each test
        task_manager.clear_all_tasks()  # Ensures a clean slate for each test


if __name__ == "__main__":
    unittest.main()
