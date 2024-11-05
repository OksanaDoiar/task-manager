import unittest
from flask import json

from app import task_manager, STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND, app
from models.task import Task


class UpdateTaskFieldsTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client for Flask
        self.app = app.test_client()
        self.app.testing = True

        # Clear existing tasks for a clean test environment
        task_manager.clear_all_tasks()  # Assumes `clear_all_tasks()` resets tasks for testing

    def test_update_single_field_success(self):
        # Add a task to update a single field
        task = Task(title="Initial Title", description="Initial Description", status="pending")
        task_manager.add_task(task)

        # Update only the title field
        update_data = {"title": "Updated Title"}

        # Call the endpoint
        response = self.app.patch(f'/tasks/{task.id}/fields', data=json.dumps(update_data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(response.get_json(), {"message": "Task fields: title has been successfully updated"})

        # Verify the task title has been updated
        updated_task = task_manager.get_task_by_id(task.id)
        self.assertEqual(updated_task.title, "Updated Title")
        self.assertEqual(updated_task.description, "Initial Description")
        self.assertEqual(updated_task.status, "pending")

    def test_update_multiple_fields_success(self):
        # Add a task to update multiple fields
        task = Task(title="Initial Title", description="Initial Description", status="pending")
        task_manager.add_task(task)

        # Update title and status fields
        update_data = {"title": "New Title", "status": "completed"}

        # Call the endpoint
        response = self.app.patch(f'/tasks/{task.id}/fields', data=json.dumps(update_data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(response.get_json(), {"message": "Task fields: title,status has been successfully updated"})

        # Verify the task fields have been updated
        updated_task = task_manager.get_task_by_id(task.id)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.status, "completed")
        self.assertEqual(updated_task.description, "Initial Description")

    def test_update_no_fields_provided(self):
        # Add a task to attempt an update with no fields
        task = Task(title="Initial Title", description="Initial Description", status="pending")
        task_manager.add_task(task)

        # Empty data payload
        update_data = {}

        # Call the endpoint
        response = self.app.patch(f'/tasks/{task.id}/fields', data=json.dumps(update_data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, STATUS_BAD_REQUEST)
        self.assertEqual(response.get_json(), {"error": "No fields provided"})

    def test_update_task_not_found(self):
        # Attempt to update fields for a non-existent task
        non_existent_task_id = 999  # Assumed to be non-existent for the test
        update_data = {"title": "New Title", "status": "completed"}

        # Call the endpoint
        response = self.app.patch(f'/tasks/{non_existent_task_id}/fields', data=json.dumps(update_data), content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, STATUS_NOT_FOUND)
        self.assertEqual(response.get_json(), {"error": "Task not found"})

    def tearDown(self):
        # Clear tasks after each test
        task_manager.clear_all_tasks()  # Ensures a clean slate for each test

if __name__ == "__main__":
    unittest.main()
