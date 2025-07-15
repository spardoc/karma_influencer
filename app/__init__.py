from flask import Flask
from app.config import Config
from app.models import db
from app.routes.api import bp as api_bp  # <-- importa la ruta
from app.routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Registra blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)

    return app