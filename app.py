from flask import Flask, request, jsonify

from models.task import Task

app = Flask(__name__)

tasks = []
generated_task_id = 1


@app.route('/', methods=['GET'])
def get_tasks():
    return jsonify([task.to_dict() for task in tasks]), 200


# GET POST PUT DELETE
@app.route('/tasks', methods=['POST'])
def create_task():
    global generated_task_id

    data = request.json

    if 'title' not in data:
        return jsonify({"error": "No title provided"}), 400

    if 'description' not in data:
        return jsonify({"error": "No description provided"}), 400

    if 'status' not in data:
        return jsonify({"error": "No status provided"}), 400

    task = Task(id=generated_task_id, title=data['title'], description=data['description'], status=data['status'])
    generated_task_id += 1
    tasks.append(task)
    return jsonify({"id": task.id}), 201


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    matched_task_index = None
    for index, task in enumerate(tasks):
        if task.id == task_id:
            matched_task_index = index

    if matched_task_index is None:
        return jsonify({"error": "Task not found"}), 404

    del tasks[matched_task_index]
    return jsonify({"message": "Task has been successfully deleted"}), 204


@app.route('/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    data = request.json

    if 'status' not in data:
        return jsonify({"error": "No status provided"}), 400

    new_status = data["status"]

    matched_task: Task = None
    for index, task in enumerate(tasks):
        if task.id == task_id:
            matched_task = task

    if matched_task is None:
        return jsonify({"error": "Task not found"}), 404

    matched_task.status = new_status
    return jsonify({"message": "Task status has been successfully updated"}), 200


@app.route('/tasks/<int:task_id>/fields', methods=['PATCH'])
def update_task_fields(task_id):
    data = request.json

    if 'status' not in data and 'title' not in data and 'description' not in data:
        return jsonify({"error": "No fields provided"}), 400

    matched_task: Task = None
    for index, task in enumerate(tasks):
        if task.id == task_id:
            matched_task = task

    if matched_task is None:
        return jsonify({"error": "Task not found"}), 404

    updated_fields = []
    for field in ['title', 'status', 'description']:
        if field in data:
            updated_fields.append(field)
            field_value = data[field]

            if field == 'title':
                matched_task.title = field_value
            elif field == 'status':
                matched_task.status = field_value
            else:
                matched_task.description = field_value

    return jsonify({"message": "Task fields: {} has been successfully updated".format(','.join(updated_fields))}), 200


if __name__ == '__main__':
    app.run(debug=True)
