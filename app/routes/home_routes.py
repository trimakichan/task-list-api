from flask import Blueprint

bp = Blueprint("home_bp", __name__)


@bp.get("/")
def home_page():
    return "<h1>✨Welcome to Makiko’s Task List API✨</h1>"