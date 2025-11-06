from flask import Blueprint

bp = Blueprint("home_bp", __name__)


@bp.get("/")
def home():
    return "<h1> Welcome to Makiko’s Task & Goal Search! </h1>"