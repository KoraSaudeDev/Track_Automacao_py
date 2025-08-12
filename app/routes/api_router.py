from flask import Blueprint
from flask import jsonify
#from app.db.querys import DBHMS

track_bp = Blueprint("track_bp",__name__)

@track_bp.route('/')
def hello():
    return "A aplicação está rodando....."


#@track_bp.route('/teste')
#def teste():
#    result = DBHMS.DB_HMS()
#    return jsonify(result)