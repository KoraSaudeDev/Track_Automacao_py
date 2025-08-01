from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    FLASK_MOD           = getenv("FLASK_MOD")
    DB_HOST             = getenv("DB_HOST")
    DB_PORT             = getenv("DB_PORT")
    DB_NAME             = getenv("DB_NAME")
    DB_USERNAME         = getenv("DB_USERNAME")
    DB_PASSWORD         = getenv("DB_PASSWORD")
    API_TOKEN           = getenv("API_TOKEN")
    ORGANIZATION_UUID   = getenv("ORGANIZATION_UUID")
    
      