import unittest

from app import app, task_manager, STATUS_NOT_FOUND, STATUS_OK
from models.task import Task


class DeleteTaskTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client for Flask
        self.app = app.test_client()
        self.app.testing = True

        # Clear existing tasks for a clean test environment
        task_manager.clear_all_tasks()  # Assumes `clear_all_tasks()` resets tasks for testing

    def test_delete_task_success(self):
        # Add a task to delete later
        task = Task(title="Sample Task", description="Task to be deleted", status="pending")
        task_manager.add_task(task)

        # Call the endpoint to delete the task
        response = self.app.delete(f'/tasks/{task.id}')

        # Assertions
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(response.get_json(), {"message": "Task has been successfully deleted"})
        # Verify the task no longer exists
        self.assertIsNone(task_manager.get_task_by_id(task.id))

    def test_delete_task_not_found(self):
        # Attempt to delete a non-existent task ID
        non_existent_task_id = 999  # Assumed to be non-existent for the test
        response = self.app.delete(f'/tasks/{non_existent_task_id}')

        # Assertions
        self.assertEqual(response.status_code, STATUS_NOT_FOUND)
        self.assertEqual(response.get_json(), {"error": "Task not found"})

    def tearDown(self):
        # Clear tasks after each test
        task_manager.clear_all_tasks()  # Ensures a clean slate for each test

if __name__ == "__main__":
    unittest.main()
