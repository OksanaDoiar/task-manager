from flask import Flask, request, jsonify

from models.task import Task
from models.task_manager import TaskManager

STATUS_NOT_FOUND = 404

STATUS_CREATED = 201

STATUS_BAD_REQUEST = 400

STATUS_OK = 200

app = Flask(__name__)

task_manager = TaskManager()


@app.route('/', methods=['GET'])
def get_tasks():
    tasks = task_manager.get_tasks()
    return jsonify([task.to_dict() for task in tasks]), STATUS_OK


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json

    if 'title' not in data:
        return jsonify({"error": "No title provided"}), STATUS_BAD_REQUEST

    if 'description' not in data:
        return jsonify({"error": "No description provided"}), STATUS_BAD_REQUEST

    if 'status' not in data:
        return jsonify({"error": "No status provided"}), STATUS_BAD_REQUEST

    task = Task(title=data['title'], description=data['description'], status=data['status'])
    task_manager.add_task(task)

    return jsonify({"id": task.id}), STATUS_CREATED


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = task_manager.get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), STATUS_NOT_FOUND

    task_manager.delete_task_by_id(task_id)
    return jsonify({"message": "Task has been successfully deleted"}), STATUS_OK


@app.route('/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    data = request.json

    if 'status' not in data:
        return jsonify({"error": "No status provided"}), STATUS_BAD_REQUEST

    new_status = data["status"]

    task = task_manager.get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), STATUS_NOT_FOUND

    task.status = new_status
    return jsonify({"message": "Task status has been successfully updated"}), STATUS_OK


@app.route('/tasks/<int:task_id>/fields', methods=['PATCH'])
def update_task_fields(task_id):
    data = request.json

    if 'status' not in data and 'title' not in data and 'description' not in data:
        return jsonify({"error": "No fields provided"}), STATUS_BAD_REQUEST

    task = task_manager.get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), STATUS_NOT_FOUND

    updated_fields = []
    for field in ['title', 'status', 'description']:
        if field in data:
            updated_fields.append(field)
            field_value = data[field]
            if field == 'title':
                task.title = field_value
            elif field == 'status':
                task.status = field_value
            else:
                task.description = field_value

    return jsonify({"message": "Task fields: {} has been successfully updated".format(','.join(updated_fields))}), STATUS_OK


if __name__ == '__main__':
    app.run(debug=True)
