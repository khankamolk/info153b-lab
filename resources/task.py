from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import TaskSchema
from models import TaskModel

task_blp = Blueprint("tasks", __name__, url_prefix="/v1/tasks", description="Tasks APIs")

@task_blp.route("/", methods=["POST", "GET"])
class TaskListAPI(MethodView):
    # POST method to create a new task
    @task_blp.arguments(TaskSchema)
    @task_blp.response(201, TaskSchema)
    def post(self, task_data):
        user_email = task_data.pop("user_email", None)
        new_task = TaskModel(**task_data)
        new_task.user_email = user_email

        # Add new_task to the database session and commit changes
        db.session.add(new_task)
        db.session.commit()

        return new_task, 201

    # GET method to retrieve all tasks
    @task_blp.response(200, TaskSchema(many=True))
    def get(self):
        tasks = TaskModel.query.all()
        return tasks

@task_blp.route("/<int:task_id>", methods=["GET", "PUT", "DELETE"])
class TaskAPI(MethodView):
    # GET method to retrieve a specific task
    @task_blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        return task

    # PUT method to edit a specific task
    @task_blp.arguments(TaskSchema)
    @task_blp.response(204)
    def put(self, task_data, task_id):
        task = TaskModel.query.get_or_404(task_id)
        task.title = task_data.get("title", task.title)
        task.is_completed = task_data.get("is_completed", task.is_completed)
        db.session.commit()
        return None, 204

    # DELETE method to delete a specific task
    @task_blp.response(204)
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return None, 204

@task_blp.route("/bulk", methods=["POST", "DELETE"])
class TaskBulkAPI(MethodView):
    # POST method to bulk add tasks
    @task_blp.arguments(TaskSchema(many=True))
    @task_blp.response(201, TaskSchema(many=True))
    def post(self, tasks_data):
        new_tasks = []
        for task_data in tasks_data:
            new_task = TaskModel(**task_data)
            db.session.add(new_task)
            new_tasks.append(new_task)
        db.session.commit()
        return new_tasks, 201

    # DELETE method to bulk delete tasks
    @task_blp.arguments(TaskSchema(many=True))
    @task_blp.response(204)
    def delete(self, tasks_data):
        for task_data in tasks_data:
            task_id = task_data.get("id")
            task = TaskModel.query.get(task_id)
            if task:
                db.session.delete(task)
        db.session.commit()
        return None, 204
