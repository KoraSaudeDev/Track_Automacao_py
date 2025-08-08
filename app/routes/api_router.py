from flask import Blueprint
from app.db.querys import ING_OTO

track_bp = Blueprint("track_bp",__name__)

@track_bp.route('/')
def hello():
    return "O bot está funcionando....."


