import sqlite3
from flask import g
import os

def get_db():
    if 'db' not in g:
        # Asegurarse de que la carpeta instance existe
        os.makedirs('instance', exist_ok=True)
        
        g.db = sqlite3.connect(
            'instance/database.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    with open('schema.sql', 'r') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)