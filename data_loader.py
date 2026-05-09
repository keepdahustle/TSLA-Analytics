"""Load CSV data dan insert ke PostgreSQL"""
import csv
from datetime import datetime
import logging
from database import execute_many, execute_query, execute_update
from migrations.init_schema import create_tables

logger = logging.getLogger(__name__)

def load_tesla_stock_data(csv_path):
    """Load Tesla stock data dari CSV ke database"""
    try:
        create_tables()
        
        data = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date_obj = datetime.strptime(row['Date'], '%Y-%m-%d').date()
                year = date_obj.year
                quarter = (date_obj.month - 1) // 3 + 1
                month = date_obj.month
                
                data.append((
                    date_obj,
                    float(row['Close']),
                    float(row['High']),
                    float(row['Low']),
                    float(row['Open']),
                    int(row['Volume']),
                    year,
                    quarter,
                    month
                ))
        
        # Batch insert
        query = """
            INSERT INTO tesla_stock_data 
            (date, close, high, low, open, volume, year, quarter, month)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (date) DO NOTHING;
        """
        
        rows_inserted = execute_many(query, data)
        logger.info(f"Inserted {rows_inserted} rows into tesla_stock_data")
        return rows_inserted
        
    except Exception as e:
        logger.error(f"Error loading Tesla stock data: {e}")
        raise

def load_model_evaluation(csv_path):
    """Load model evaluation dari CSV ke database"""
    try:
        data = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append((
                    row['Model'],
                    float(row['MAE']),
                    float(row['RMSE']),
                    float(row['MAPE (%)']),
                    float(row['R²']),
                    float(row['Dir Accuracy']),
                    float(row['Dir Precision']),
                    float(row['Dir Recall']),
                    float(row['Dir F1'])
                ))
        
        query = """
            INSERT INTO model_evaluation 
            (model, mae, rmse, mape_percentage, r_squared, dir_accuracy, dir_precision, dir_recall, dir_f1)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (model) DO UPDATE SET
                mae = EXCLUDED.mae,
                rmse = EXCLUDED.rmse,
                mape_percentage = EXCLUDED.mape_percentage,
                r_squared = EXCLUDED.r_squared,
                dir_accuracy = EXCLUDED.dir_accuracy,
                dir_precision = EXCLUDED.dir_precision,
                dir_recall = EXCLUDED.dir_recall,
                dir_f1 = EXCLUDED.dir_f1;
        """
        
        rows_inserted = execute_many(query, data)
        logger.info(f"Inserted {rows_inserted} rows into model_evaluation")
        return rows_inserted
        
    except Exception as e:
        logger.error(f"Error loading model evaluation: {e}")
        raise

def load_predictions_sarima(csv_path):
    """Load SARIMA predictions dari CSV ke database"""
    try:
        data = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date_obj = datetime.strptime(row['Date'], '%Y-%m-%d').date()
                data.append((
                    date_obj,
                    float(row['Actual']),
                    float(row['SARIMA_Pred'])
                ))
        
        query = """
            INSERT INTO predictions_sarima 
            (date, actual, sarima_pred)
            VALUES (%s, %s, %s)
            ON CONFLICT (date) DO NOTHING;
        """
        
        rows_inserted = execute_many(query, data)
        logger.info(f"Inserted {rows_inserted} rows into predictions_sarima")
        return rows_inserted
        
    except Exception as e:
        logger.error(f"Error loading SARIMA predictions: {e}")
        raise

def load_predictions_prophet(csv_path):
    """Load Prophet predictions dari CSV ke database"""
    try:
        data = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date_obj = datetime.strptime(row['Date'], '%Y-%m-%d').date()
                data.append((
                    date_obj,
                    float(row['Actual']),
                    float(row['Prophet_Pred'])
                ))
        
        query = """
            INSERT INTO predictions_prophet 
            (date, actual, prophet_pred)
            VALUES (%s, %s, %s)
            ON CONFLICT (date) DO NOTHING;
        """
        
        rows_inserted = execute_many(query, data)
        logger.info(f"Inserted {rows_inserted} rows into predictions_prophet")
        return rows_inserted
        
    except Exception as e:
        logger.error(f"Error loading Prophet predictions: {e}")
        raise

def initialize_database(data_dir="../"):
    """Initialize database dengan semua data dari CSV"""
    try:
        logger.info("Starting database initialization...")
        
        # Create tables
        create_tables()
        
        # Load data
        load_tesla_stock_data(f"{data_dir}/Tesla_stock_data.csv")
        load_model_evaluation(f"{data_dir}/model_evaluation.csv")
        load_predictions_sarima(f"{data_dir}/predictions_sarima.csv")
        load_predictions_prophet(f"{data_dir}/predictions_prophet.csv")
        
        logger.info("Database initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    initialize_database()
