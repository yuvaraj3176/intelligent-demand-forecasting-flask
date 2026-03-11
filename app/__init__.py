from flask import Flask
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure data directory exists
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    
    # Register routes
    from app import routes
    routes.init_app(app)
    
    return app