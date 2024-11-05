import unittest

from app import task_manager, STATUS_OK, app
from models.task import Task


class GetTasksTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client for Flask
        self.app = app.test_client()
        self.app.testing = True

        # Clear existing tasks for a clean test environment
        task_manager.clear_all_tasks()  # Assumes `clear_all_tasks()` resets tasks for testing

    def test_get_tasks_empty(self):
        # Ensure the task list is empty
        response = self.app.get('/')

        # Assertions
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(response.get_json(), [])  # Expecting an empty list when no tasks exist

    def test_get_tasks_with_data(self):
        # Add some tasks to the task manager
        task1 = Task(title="Task 1", description="First task", status="pending")
        task2 = Task(title="Task 2", description="Second task", status="completed")
        task_manager.add_task(task1)
        task_manager.add_task(task2)

        # Call the endpoint to get tasks
        response = self.app.get('/')

        # Assertions
        self.assertEqual(response.status_code, STATUS_OK)

        # Get JSON response and validate contents
        tasks = response.get_json()
        self.assertEqual(len(tasks), 2)

        # Check the first task's content
        self.assertEqual(tasks[0]["title"], "Task 1")
        self.assertEqual(tasks[0]["description"], "First task")
        self.assertEqual(tasks[0]["status"], "pending")

        # Check the second task's content
        self.assertEqual(tasks[1]["title"], "Task 2")
        self.assertEqual(tasks[1]["description"], "Second task")
        self.assertEqual(tasks[1]["status"], "completed")

    def tearDown(self):
        # Clear tasks after each test
        task_manager.clear_all_tasks()  # Ensures a clean slate for each test


if __name__ == "__main__":
    unittest.main()
