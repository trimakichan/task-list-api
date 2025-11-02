from flask import Blueprint, abort, make_response, request, Response
from datetime import datetime
from app.models.task import Task
from .route_utilities import validate_model
from ..db import db

bp = Blueprint("bp", __name__, url_prefix="/tasks")

@bp.get("")
def get_all_tasks():
    sort_param = request.args.get("sort")
    query = db.select(Task)
    
    if sort_param:
        sort_param = sort_param.casefold().strip() 
        if sort_param in ("asc", "desc"):
            query = Task.sort_by_title(query, sort_param)
        else:
            invalid_msg = {"message": "Invalid sort value. Valid options: asc, desc."}
            abort(make_response(invalid_msg, 400))
    
    tasks = db.session.scalars(query.order_by(Task.id))

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return tasks_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task,task_id)
    return task.to_dict()

@bp.post("")
def create_task():
    request_body = request.get_json()
    # check_request_body(request_body)
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task,task_id)
    request_body = request.get_json()
    # check_request_body(request_body)
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_complete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task,task_id)
    
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# def check_request_body(request_body):
#     try:
#         request_body["title"]
#         request_body["description"]
#     except KeyError:
#         abort(make_response({"details": "Invalid data"}, 400))
