from flask import Blueprint, request, abort, make_response, Response
from .route_utilities import validate_model, create_model, update_model, get_models_with_filters
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

    return goal.to_dict(ids_only=True)

@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, filters=request.args)

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
    required_keys = ["title"]
    return update_model(Goal, goal_id, required_keys)

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")