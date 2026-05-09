"""Database connection dan utilities untuk PostgreSQL"""
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
import logging
from config import DB_CONFIG, POOL_SIZE, MAX_OVERFLOW, POOL_TIMEOUT, POOL_RECYCLE, CONNECT_TIMEOUT, COMMAND_TIMEOUT

logger = logging.getLogger(__name__)

# Connection Pool
_pool = None

def init_pool():
    """Initialize connection pool"""
    global _pool
    try:
        if _pool is not None:
            return
        _pool = SimpleConnectionPool(
            1,
            POOL_SIZE,
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            connect_timeout=CONNECT_TIMEOUT,
            options="-c statement_timeout=30000"  # 30 second query timeout
        )
        logger.info("Database connection pool initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize connection pool: {e}")
        raise

def get_connection():
    """Get connection dari pool"""
    global _pool
    if _pool is None:
        init_pool()
    return _pool.getconn()

def return_connection(conn):
    """Return connection ke pool"""
    global _pool
    if _pool:
        _pool.putconn(conn)

def close_all_connections():
    """Close semua connections di pool"""
    global _pool
    if _pool:
        _pool.closeall()

def execute_query(query, params=None, fetch_one=False, fetch_all=True):
    """Execute SELECT query dengan connection pooling"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = None
            
        cursor.close()
        return result
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        raise
    finally:
        if conn:
            return_connection(conn)

def execute_update(query, params=None):
    """Execute INSERT/UPDATE/DELETE query"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Update execution error: {e}")
        raise
    finally:
        if conn:
            return_connection(conn)

def execute_many(query, data):
    """Execute batch INSERT/UPDATE"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executemany(query, data)
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Batch execution error: {e}")
        raise
    finally:
        if conn:
            return_connection(conn)
