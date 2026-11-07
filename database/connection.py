"""
MARKETIX Database Connection Manager
Provides PostgreSQL connectivity with robust health checks and informative diagnostics.
Supports SQLite fallback for local testing when PostgreSQL server is offline.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

logger = logging.getLogger("marketix.db")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "marketix")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
SQLITE_DB_PATH = BASE_DIR / os.getenv("SQLITE_DB_PATH", "database/marketix.db")

POSTGRES_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLITE_URL = f"sqlite:///{SQLITE_DB_PATH}"

_engine = None
_db_type = None
_connection_status = {"connected": False, "type": None, "message": "Not initialized"}


def get_db_status():
    """Returns the current database connection status and diagnostics."""
    global _connection_status
    test_connection()
    return _connection_status


def test_connection():
    """Tests connection to PostgreSQL and falls back gracefully to SQLite if needed."""
    global _engine, _db_type, _connection_status

    # Try PostgreSQL first
    try:
        pg_engine = create_engine(POSTGRES_URL, connect_args={"connect_timeout": 3})
        with pg_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        _engine = pg_engine
        _db_type = "PostgreSQL"
        _connection_status = {
            "connected": True,
            "type": "PostgreSQL",
            "message": f"Connected to PostgreSQL database '{DB_NAME}' at {DB_HOST}:{DB_PORT}",
            "is_postgres": True,
        }
        return _engine
    except Exception as pg_err:
        # Informative notice without dumping raw psycopg2 stack traces to terminal
        logger.info(f"PostgreSQL server not detected on {DB_HOST}:{DB_PORT}. Activating embedded SQLite database.")
        try:
            SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            sqlite_engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
            with sqlite_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            _engine = sqlite_engine
            _db_type = "SQLite"
            _connection_status = {
                "connected": True,
                "type": "SQLite (Local Fallback)",
                "message": (
                    f"PostgreSQL daemon offline. "
                    f"Using local embedded SQLite database at {SQLITE_DB_PATH.name} for uninterrupted operation."
                ),
                "is_postgres": False,
                "pg_error": str(pg_err),
            }
            return _engine
        except Exception as sqlite_err:
            _connection_status = {
                "connected": False,
                "type": None,
                "message": f"Database unavailable. Postgres error: {pg_err}. SQLite error: {sqlite_err}",
                "is_postgres": False,
                "pg_error": str(pg_err),
            }
            return None


def get_engine():
    """Returns the active SQLAlchemy database engine."""
    global _engine
    if _engine is None:
        test_connection()
    return _engine


def get_session():
    """Returns a new SQLAlchemy session."""
    engine = get_engine()
    if engine is None:
        raise ConnectionError("Database unavailable. Please check database configuration.")
    Session = sessionmaker(bind=engine)
    return Session()


def init_db():
    """Initializes schema tables in the database."""
    engine = get_engine()
    if engine is None:
        return False, "Database unavailable"

    schema_file = BASE_DIR / "database" / "schema.sql"
    if not schema_file.exists():
        return False, f"Schema file not found at {schema_file}"

    try:
        with open(schema_file, "r") as f:
            sql_content = f.read()

        # In SQLite, convert PostgreSQL-specific syntax if running on SQLite
        if _db_type == "SQLite":
            # Adjust PostgreSQL syntax for SQLite compatibility
            sql_statements = []
            for stmt in sql_content.split(";"):
                stmt = stmt.strip()
                if not stmt:
                    continue
                # Replace Postgres-specific keywords
                cleaned_stmt = stmt.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
                cleaned_stmt = cleaned_stmt.replace("DROP TABLE IF EXISTS predictions CASCADE", "DROP TABLE IF EXISTS predictions")
                cleaned_stmt = cleaned_stmt.replace("DROP TABLE IF EXISTS customer_segments CASCADE", "DROP TABLE IF EXISTS customer_segments")
                cleaned_stmt = cleaned_stmt.replace("DROP TABLE IF EXISTS campaign_responses CASCADE", "DROP TABLE IF EXISTS campaign_responses")
                cleaned_stmt = cleaned_stmt.replace("DROP TABLE IF EXISTS campaigns CASCADE", "DROP TABLE IF EXISTS campaigns")
                cleaned_stmt = cleaned_stmt.replace("DROP TABLE IF EXISTS customers CASCADE", "DROP TABLE IF EXISTS customers")
                cleaned_stmt = cleaned_stmt.replace("DROP TABLE IF EXISTS dataset_uploads CASCADE", "DROP TABLE IF EXISTS dataset_uploads")
                cleaned_stmt = cleaned_stmt.replace("TIMESTAMP DEFAULT CURRENT_TIMESTAMP", "DATETIME DEFAULT CURRENT_TIMESTAMP")
                sql_statements.append(cleaned_stmt)

            with engine.begin() as conn:
                for stmt in sql_statements:
                    if stmt:
                        try:
                            conn.execute(text(stmt))
                        except Exception as e:
                            logger.warning(f"Notice executing statement in SQLite: {e}")
        else:
            with engine.begin() as conn:
                for stmt in sql_content.split(";"):
                    stmt = stmt.strip()
                    if stmt:
                        conn.execute(text(stmt))

        return True, f"Database initialized successfully ({_db_type})"
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False, str(e)
