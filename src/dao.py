"""
Simple SQLite persistence for predictions and results.
"""
import sqlite3
import os
from datetime import datetime

class PredictionDB:
    def __init__(self, database_url=None):
        # expects sqlite:///path/to/db
        if database_url and database_url.startswith('sqlite:///'):
            path = database_url.replace('sqlite:///','')
        else:
            path = 'data/predictions.db'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._ensure_tables()

    def _ensure_tables(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id TEXT PRIMARY KEY,
                created_at TEXT,
                home TEXT,
                away TEXT,
                match_time TEXT,
                competition TEXT,
                payload TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id TEXT PRIMARY KEY,
                prediction_id TEXT,
                home_goals INTEGER,
                away_goals INTEGER,
                recorded_at TEXT
            )
        ''')
        self.conn.commit()

    def insert_prediction(self, result):
        import uuid, json
        pid = str(uuid.uuid4())
        c = self.conn.cursor()
        c.execute('INSERT INTO predictions (id, created_at, home, away, match_time, competition, payload) VALUES (?,?,?,?,?,?,?)',
                  (pid, datetime.utcnow().isoformat(), result['match']['home'], result['match']['away'], result['match']['match_time'], result['match'].get('competition'), json.dumps(result)))
        self.conn.commit()
        # return stored id
        return pid

    def insert_result(self, prediction_id, home_goals, away_goals):
        import uuid
        pid = str(uuid.uuid4())
        c = self.conn.cursor()
        c.execute('INSERT INTO results (id, prediction_id, home_goals, away_goals, recorded_at) VALUES (?,?,?,?,?)',
                  (pid, prediction_id, home_goals, away_goals, datetime.utcnow().isoformat()))
        self.conn.commit()
        return pid
