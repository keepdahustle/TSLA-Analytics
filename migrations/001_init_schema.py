"""Initial database schema creation"""
import logging
from database import execute_update, get_connection

logger = logging.getLogger(__name__)

def create_tables():
    """Create all required tables"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Drop existing tables if needed (optional, comment out for production)
        # cursor.execute("DROP TABLE IF EXISTS predictions_prophet CASCADE;")
        # cursor.execute("DROP TABLE IF EXISTS predictions_sarima CASCADE;")
        # cursor.execute("DROP TABLE IF EXISTS model_evaluation CASCADE;")
        # cursor.execute("DROP TABLE IF EXISTS tesla_stock_data CASCADE;")
        
        # Create tesla_stock_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tesla_stock_data (
                id SERIAL PRIMARY KEY,
                date DATE UNIQUE NOT NULL,
                close FLOAT NOT NULL,
                high FLOAT NOT NULL,
                low FLOAT NOT NULL,
                open FLOAT NOT NULL,
                volume BIGINT NOT NULL,
                year INT,
                quarter INT,
                month INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_tesla_date ON tesla_stock_data(date);
        """)
        
        # Create model_evaluation table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_evaluation (
                id SERIAL PRIMARY KEY,
                model VARCHAR(50) UNIQUE NOT NULL,
                mae FLOAT NOT NULL,
                rmse FLOAT NOT NULL,
                mape_percentage FLOAT NOT NULL,
                r_squared FLOAT NOT NULL,
                dir_accuracy FLOAT NOT NULL,
                dir_precision FLOAT NOT NULL,
                dir_recall FLOAT NOT NULL,
                dir_f1 FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create predictions_sarima table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions_sarima (
                id SERIAL PRIMARY KEY,
                date DATE UNIQUE NOT NULL,
                actual FLOAT NOT NULL,
                sarima_pred FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_date (date)
            );
        """)
        
        # Create predictions_prophet table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions_prophet (
                id SERIAL PRIMARY KEY,
                date DATE UNIQUE NOT NULL,
                actual FLOAT NOT NULL,
                prophet_pred FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_date (date)
            );
        """)
        
        conn.commit()
        logger.info("Tables created successfully")
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error creating tables: {e}")
        raise
    finally:
        if conn:
            from database import return_connection
            return_connection(conn)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_tables()
