import os

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'cambiar_en_produccion')

    # Base de datos SQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///data/karma.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Rutas CSV (si se usa CSV en lugar de BD)
    CSV_DIR = os.getenv('CSV_DIR', 'data')
    INFLUENCERS_CSV = os.path.join(CSV_DIR, 'influencers.csv')
    COMMENTS_CSV = os.path.join(CSV_DIR, 'comments.csv')

    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')