from flask import Blueprint


track_bp = Blueprint("track_bp",__name__)

@track_bp.route('/')
def hello():
    with open("system.log", "r") as f:
        log_content = f.read()
    return f"<pre>{log_content}</pre>"


