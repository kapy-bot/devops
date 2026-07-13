import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Read the connection string from the environment rather than hardcoding it,
# so the same image works locally (docker-compose), and later in AKS
# (via a K8s Secret/ConfigMap) without a rebuild.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://todo:todo@localhost:5432/todo"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
