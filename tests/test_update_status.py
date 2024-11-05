import unittest
from flask import json

from app import app, task_manager, STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND
from models.task import Task


class UpdateTaskStatusTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client for Flask
        self.app = app.test_client()
        self.app.testing = True

        # Clear existing tasks for a clean test environment
        task_manager.clear_all_tasks()  # Assumes `clear_all_tasks()` resets tasks for testing

    def test_update_task_status_success(self):
        # Add a task to update its status later
        task = Task(title="Sample Task", description="Task to update status", status="pending")
        task_manager.add_task(task)

        # Data for updating the task status
        update_data = {
            "status": "completed"
        }

        # Call the endpoint to update the task's status
        response = self.app.put(f'/tasks/{task.id}/status', data=json.dumps(update_data),
                                content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(response.get_json(), {"message": "Task status has been successfully updated"})

        # Verify the status has been updated in the task_manager
        updated_task = task_manager.get_task_by_id(task.id)
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.status, "completed")

    def test_update_task_status_missing_status(self):
        # Add a task to attempt an update without 'status'
        task = Task(title="Sample Task", description="Task to update status", status="pending")
        task_manager.add_task(task)

        # Data with missing 'status' field
        update_data = {}

        # Call the endpoint to update the task's status
        response = self.app.put(f'/tasks/{task.id}/status', data=json.dumps(update_data),
                                content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, STATUS_BAD_REQUEST)
        self.assertEqual(response.get_json(), {"error": "No status provided"})

    def test_update_task_status_task_not_found(self):
        # Attempt to update the status of a non-existent task
        non_existent_task_id = 999  # Assumed to be non-existent for the test
        update_data = {
            "status": "completed"
        }

        # Call the endpoint to update the non-existent task's status
        response = self.app.put(f'/tasks/{non_existent_task_id}/status', data=json.dumps(update_data),
                                content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, STATUS_NOT_FOUND)
        self.assertEqual(response.get_json(), {"error": "Task not found"})

    def tearDown(self):
        # Clear tasks after each test
        task_manager.clear_all_tasks()  # Ensures a clean slate for each test


if __name__ == "__main__":
    unittest.main()
