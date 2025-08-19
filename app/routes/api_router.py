from flask import Blueprint
from flask import jsonify
#from app.db.querys import DBHMS

track_bp = Blueprint("track_bp",__name__)

@track_bp.route('/')
def hello():
    with open("system.log", "r") as f:
        log_content = f.read()
    return f"<pre>{log_content}</pre>"


#@track_bp.route('/teste')
#def teste():
#    result = DBHMS.DB_HMS()
#    return jsonify(result)