from flask import Blueprint
from app.controllers import api_controller
from app.db.querys import ING_OTO

track_bp = Blueprint("track_bp",__name__)

@track_bp.route('/')
def hello():
    return "O bot está funcionando....."

#track_bp.add_url_rule('/',view_func=api_controller.getSurveys)
#track_bp.add_url_rule('/add',view_func=api_controller.postDistribution)
track_bp.add_url_rule('/teste',view_func=ING_OTO.DB_ING_OTO)
