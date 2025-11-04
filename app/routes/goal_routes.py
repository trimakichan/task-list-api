from flask import Blueprint, request, abort, make_response, Response
from .route_utilities import validate_model, create_model
from ..models.goal import Goal
from ..models.task import Task
from app.db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.post("/<goal_id>/tasks")
def create_task_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    try:
        task_ids = request_body["task_ids"]
    except KeyError as error:
        invalid_msg = {"details": "Invalid data"}
        abort(make_response(invalid_msg, 400))

    tasks = [validate_model(Task, task_id) for task_id in task_ids]
    
    goal.tasks = tasks
    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }

    return response

@bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query.order_by(Goal.id))

    goals_response = [goal.to_dict() for goal in goals]
    return goals_response

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict()

@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(include_tasks=True)


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    try:
        goal.title = request_body["title"]
    except KeyError:
        invalid_msg = {"details": "Invalid data"}
        abort(make_response(invalid_msg, 400))
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_goal(task_id):
    goal = validate_model(Goal, task_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")