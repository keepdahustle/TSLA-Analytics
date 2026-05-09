#!/usr/bin/env python
"""Setup script untuk initialize database dan load data"""
import os
import sys
import logging
from pathlib import Path

# Add current directory to path
current_file = os.path.abspath(__file__)
script_dir = os.path.dirname(current_file)
sys.path.insert(0, script_dir)

try:
    from database import init_pool, close_all_connections
    from migrations.init_schema import create_tables
    from data_loader import (
        load_tesla_stock_data,
        load_model_evaluation,
        load_predictions_sarima,
        load_predictions_prophet
    )
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    print(f"[DEBUG] script_dir: {script_dir}")
    print(f"[DEBUG] sys.path: {sys.path}")
    raise

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main setup function"""
    try:
        logger.info("Starting database setup...")
        
        # Get data directory path
        current_dir = Path(script_dir)
        
        # Try to find CSV files
        csv_paths = {
            "Tesla_stock_data.csv": None,
            "model_evaluation.csv": None,
            "predictions_sarima.csv": None,
            "predictions_prophet.csv": None
        }
        
        # Check in parent directory (production)
        for csv_name in csv_paths.keys():
            parent_path = current_dir.parent / csv_name
            if parent_path.exists():
                csv_paths[csv_name] = str(parent_path)
                logger.info(f"Found {csv_name} in parent directory: {parent_path}")
        
        # Check in current directory (alternative)
        for csv_name in csv_paths.keys():
            if csv_paths[csv_name] is None:
                current_path = current_dir / csv_name
                if current_path.exists():
                    csv_paths[csv_name] = str(current_path)
                    logger.info(f"Found {csv_name} in current directory: {current_path}")
        
        # Verify all files found
        missing_files = [name for name, path in csv_paths.items() if path is None]
        if missing_files:
            logger.error(f"Missing CSV files: {', '.join(missing_files)}")
            logger.info(f"Expected files in: {current_dir} or {current_dir.parent}")
            return False
        
        # Initialize database
        logger.info("Initializing database...")
        init_pool()
        
        # Create tables
        logger.info("Creating database tables...")
        create_tables()
        
        # Load data
        logger.info("Loading data from CSV files...")
        load_tesla_stock_data(csv_paths["Tesla_stock_data.csv"])
        load_model_evaluation(csv_paths["model_evaluation.csv"])
        load_predictions_sarima(csv_paths["predictions_sarima.csv"])
        load_predictions_prophet(csv_paths["predictions_prophet.csv"])
        
        logger.info("✓ Database setup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Setup failed: {e}", exc_info=True)
        return False
    finally:
        close_all_connections()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
