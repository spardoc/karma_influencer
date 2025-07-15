# test_sqlite.py
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/karma.db")
conn = engine.connect()
print("Conexión exitosa.")
conn.close()
