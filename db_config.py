from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import  sessionmaker


# Database Configuration :-

DATABASE_URL = "sqlite:///./orders.db"  # Persistent file-based data (DB) storage
# DATABASE_URL = "sqlite:///:memory:"  # DB is stored only in RAM (process memory).

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}, # `connect_args` is for SQLite only to allow multithreaded access.
    poolclass=StaticPool,  # `StaticPool` is used for in-memory DB to ensure the same connection is used.
)

# Create a sessionmaker to generate new Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
