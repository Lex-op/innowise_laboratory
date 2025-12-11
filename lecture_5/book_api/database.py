from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator

SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=Session
)


Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session.

    Yields:
        Session: SQLAlchemy database session.

    Note:
        The session is automatically closed after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """
    Create all database tables defined in SQLAlchemy models.

    This function should be called once during application startup
    to ensure all required tables exist in the database.
    """
    Base.metadata.create_all(bind=engine)
