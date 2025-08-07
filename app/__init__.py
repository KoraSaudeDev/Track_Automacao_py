import os
from flask import Flask
from flask_cors import CORS
from .routes.api_router import track_bp
from app.controllers import api_controller
from app.db import db
from app.service import jobs



def create_app():
    app = Flask(__name__)

    db.get_connection("OTO_ING")
    jobs.schedule_task(api_controller.postDistribution)
    
    app.register_blueprint(track_bp)
    
    return app