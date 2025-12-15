from infra.db import get_engine

engine = get_engine()
with engine.connect() as conn:
    print("DB connection OK")
