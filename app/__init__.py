import os
from flask import Flask
from flask_cors import CORS
from .routes.api_router import track_bp
from .start_scheduler import start_all, start_all_teste

def create_app():
    app = Flask(__name__)
    
    #start_all_teste()
    start_all()

    app.register_blueprint(track_bp)
    
    return app