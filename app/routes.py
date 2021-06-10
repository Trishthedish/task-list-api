from flask.json import jsonify
from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify
from datetime import date, datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET","POST"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return {
                "details": f"Invalid data"
            }, 400
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"]
        )
        db.session.add(new_task)
        db.session.commit()
        if new_task.completed_at == None:
            completed_at = False
        else:
            completed_at = True
        return make_response({
            "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": completed_at
            }
        }, 201)

    elif request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title).all()
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
        else:
            tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
            if task.completed_at == None:
                completed_at = False
            else:
                completed_at = True
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": completed_at
            })
        return make_response(jsonify(tasks_response))

@tasks_bp.route("/<task_id>", methods=["GET","PUT","DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        if task.completed_at == None:
            completed_at = False
        else:
            completed_at = True
        return make_response({
            "task": {
                 "id": task.task_id,
                 "title": task.title,
                 "description": task.description,
                 "is_complete": completed_at
            }
        })

    elif request.method == "PUT":
        form_data = request.get_json()
        if ("completed_at" not in form_data or form_data["completed_at"] == None):
            is_complete = False
        else:
            is_complete = True
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        response_task = {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_complete
            }
        }
        return make_response(response_task, 200)

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        if task.completed_at == None:
            completed_at = False
        else:
            completed_at = True
        return make_response(
            {
            "details":
               f"Task {task.task_id} \"{task.title}\" successfully deleted"
            }
        )
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return  make_response("Task {task_id} not found", 404)

    task.completed_at = datetime.utcnow()
    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True
        }
    }, 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return make_response("Task {taske_id} not found", 404)
    task.completed_at = None

    db.session.commit()
    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }, 200