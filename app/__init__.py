import os
from flask import Flask
from flask_cors import CORS
from .routes.api_router import track_bp
from app.scheduler import schedulers

data = [
    {
        "name":"Carlos souza",
        "email":"Car850075@gmail.com",
        "phone":"55961102204",
        "cpf":"01010101"
    }
]

schedulers.start_schedulers(data,"e0be9e84-b80e-4f4c-93ca-f947b0a182e0")



def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(track_bp)
    
    return app