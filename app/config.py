import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'cambiar_en_produccion')

    # Base de datos SQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, '../data/karma.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Rutas CSV (si se usa CSV en lugar de BD)
    CSV_DIR = os.getenv('CSV_DIR', 'data')
    INFLUENCERS_CSV = os.path.join(CSV_DIR, 'influencers.csv')
    COMMENTS_CSV = os.path.join(CSV_DIR, 'comments.csv')

    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Reddit
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'karma_influencer_app/0.1')