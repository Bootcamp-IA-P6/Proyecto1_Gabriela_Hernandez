from sqlalchemy import text
from infra.db import get_engine

class TripRepositoryDB:
    def __init__(self, engine=None):
        self.engine = engine or get_engine()

    def save_trip(self, stopped_seconds, moving_seconds, stopped_rate, moving_rate, total_eur):
        sql = text("""
            INSERT INTO trips (stopped_seconds, moving_seconds, stopped_rate, moving_rate, total_eur)
            VALUES (:stopped, :moving, :sr, :mr, :total)
        """)
        with self.engine.begin() as conn:
            conn.execute(sql, {
                "stopped": float(stopped_seconds),
                "moving": float(moving_seconds),
                "sr": float(stopped_rate),
                "mr": float(moving_rate),
                "total": float(total_eur),
            })
