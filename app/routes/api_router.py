from flask import Blueprint
#from app.db.querys_mv.HUB_ES.HPC import DB
#import pandas as pd


track_bp = Blueprint("track_bp",__name__)

@track_bp.route('/')
def hello():
    with open("system.log", "r") as f:
        log_content = f.read()
    return f"<pre>{log_content}</pre>"


#@track_bp.route('/teste')
#def teste():
#    result = DB()
#    df = pd.DataFrame(result)
#    df.to_csv("HPC.csv", index=False)
#    return result