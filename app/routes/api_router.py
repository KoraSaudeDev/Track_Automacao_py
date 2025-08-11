from flask import Blueprint
#from app.db.querys.HMS import maternidade

track_bp = Blueprint("track_bp",__name__)

@track_bp.route('/')
def hello():
    return "O bot está funcionando....."


#track_bp.add_url_rule('/teste',view_func=maternidade.DB_HMS)