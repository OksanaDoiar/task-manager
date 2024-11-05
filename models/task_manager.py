class TaskManager:

    def __init__(self):
        self.generated_id = 1
        self.tasks = []

    def get_tasks(self):
        return self.tasks

    def add_task(self, task):
        task.id = self.generated_id
        self.generated_id += 1
        self.tasks.append(task)

    def get_task_by_id(self, task_id):
        for index, task in enumerate(self.tasks):
            if task.id == task_id:
                return task
        return None

    def delete_task_by_id(self, task_id):
        task_index = self._get_task_index_by_id(task_id)
        if task_index is None:
            return None

        del self.tasks[task_index]

    def _get_task_index_by_id(self, task_id):
        for index, task in enumerate(self.tasks):
            if task.id == task_id:
                return index
        return None