from flask import Blueprint, abort, make_response, request, Response
from datetime import datetime
import os
import requests
from app.models.task import Task
from .route_utilities import validate_model, create_model
from app.db import db


SLACK_URL = "https://slack.com/api/chat.postMessage"
SLACK_API_KEY = os.environ.get('SLACK_API_KEY')

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

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
    tasks_response = [task.to_dict() for task in tasks]

    return tasks_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task,task_id)
    
    return task.to_dict()

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task,task_id)
    request_body = request.get_json()

    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except KeyError:
        invalid_msg = {"details": "Invalid data"}
        abort(make_response(invalid_msg, 400))

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_complete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()

    db.session.commit()

    send_msg_slack(task)

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

def send_msg_slack(task):
    json_body = {
        "channel": "C09N95RPR34",
        "text": f"Someone just completed the task {task.title}"
    }

    headers = {
        "Authorization": f"Bearer {SLACK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    requests.post(SLACK_URL, json=json_body, headers=headers)

