from dotenv import load_dotenv
from app import create_app
from app.models import db
import os

load_dotenv()  # Esto carga las variables del archivo .env automáticamente

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # <-- Esto crea las tablas si no existen
    app.run(debug=True)