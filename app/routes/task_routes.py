from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.get("")
def get_all_tasks():
    sort = request.args.get("sort")
    query = db.select(Task)

    if sort == 'asc':
        query = query.order_by(Task.title)
    elif sort == 'desc':
        query = query.order_by(Task.title.desc())
    
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            task.to_dict()
        )

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)
    return task.to_dict()

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    check_request_body(request_body)
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    check_request_body(request_body)

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        invalid = {"message": f"Task {task_id} is invalid."}
        abort(make_response(invalid, 400))
    
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        not_found = {"message" : f"Task ({task_id}) is not found."}  
        abort(make_response(not_found, 404))

    return task

def check_request_body(request_body):
    try:
        request_body["title"]
        request_body["description"]
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))



