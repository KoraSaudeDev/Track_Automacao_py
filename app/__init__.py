import os
from flask import Flask
from flask_cors import CORS
from .routes.api_router import track_bp
from app.controllers import api_controller




def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(track_bp)
    
    return app