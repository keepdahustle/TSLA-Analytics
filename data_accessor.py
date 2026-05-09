"""Database helpers untuk mengakses data seperti yang diakses dari CSV"""
import pandas as pd
from database import execute_query
import logging

logger = logging.getLogger(__name__)

class DataAccessor:
    """Helper class untuk mengakses data dari PostgreSQL dengan interface seperti pandas"""
    
    @staticmethod
    def get_tesla_stock_data():
        """Get semua Tesla stock data, sorted by date"""
        try:
            query = """
                SELECT date as "Date", close as "Close", high as "High", 
                       low as "Low", open as "Open", volume as "Volume",
                       year as "Year", quarter as "Quarter", month as "Month"
                FROM tesla_stock_data
                ORDER BY date ASC;
            """
            results = execute_query(query)
            if not results:
                return pd.DataFrame()
            
            df = pd.DataFrame(results)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except Exception as e:
            logger.error(f"Error getting Tesla stock data: {e}")
            raise
    
    @staticmethod
    def get_tesla_stock_by_year(year):
        """Get Tesla stock data for specific year"""
        try:
            query = """
                SELECT date as "Date", close as "Close", high as "High", 
                       low as "Low", open as "Open", volume as "Volume"
                FROM tesla_stock_data
                WHERE year = %s
                ORDER BY date ASC;
            """
            results = execute_query(query, (year,))
            if not results:
                return pd.DataFrame()
            
            df = pd.DataFrame(results)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except Exception as e:
            logger.error(f"Error getting stock data for year {year}: {e}")
            raise
    
    @staticmethod
    def get_tesla_stock_by_year_quarter(year, quarter):
        """Get Tesla stock data for specific year and quarter"""
        try:
            query = """
                SELECT date as "Date", close as "Close", high as "High", 
                       low as "Low", open as "Open", volume as "Volume"
                FROM tesla_stock_data
                WHERE year = %s AND quarter = %s
                ORDER BY date ASC;
            """
            results = execute_query(query, (year, quarter))
            if not results:
                return pd.DataFrame()
            
            df = pd.DataFrame(results)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except Exception as e:
            logger.error(f"Error getting stock data for {year} Q{quarter}: {e}")
            raise
    
    @staticmethod
    def get_model_evaluation():
        """Get model evaluation metrics"""
        try:
            query = """
                SELECT model as "Model", mae as "MAE", rmse as "RMSE",
                       mape_percentage as "MAPE (%)", r_squared as "R²",
                       dir_accuracy as "Dir Accuracy", dir_precision as "Dir Precision",
                       dir_recall as "Dir Recall", dir_f1 as "Dir F1"
                FROM model_evaluation
                ORDER BY model ASC;
            """
            results = execute_query(query)
            if not results:
                return pd.DataFrame()
            
            return pd.DataFrame(results)
        except Exception as e:
            logger.error(f"Error getting model evaluation: {e}")
            raise
    
    @staticmethod
    def get_predictions_sarima():
        """Get SARIMA predictions"""
        try:
            query = """
                SELECT date as "Date", actual as "Actual", sarima_pred as "SARIMA_Pred"
                FROM predictions_sarima
                ORDER BY date ASC;
            """
            results = execute_query(query)
            if not results:
                return pd.DataFrame()
            
            df = pd.DataFrame(results)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except Exception as e:
            logger.error(f"Error getting SARIMA predictions: {e}")
            raise
    
    @staticmethod
    def get_predictions_prophet():
        """Get Prophet predictions"""
        try:
            query = """
                SELECT date as "Date", actual as "Actual", prophet_pred as "Prophet_Pred"
                FROM predictions_prophet
                ORDER BY date ASC;
            """
            results = execute_query(query)
            if not results:
                return pd.DataFrame()
            
            df = pd.DataFrame(results)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except Exception as e:
            logger.error(f"Error getting Prophet predictions: {e}")
            raise
    
    @staticmethod
    def get_combined_predictions():
        """Get combined predictions from both models"""
        try:
            query = """
                SELECT 
                    s.date as "Date",
                    s.actual as "Actual",
                    s.sarima_pred as "SARIMA_Pred",
                    p.prophet_pred as "Prophet_Pred"
                FROM predictions_sarima s
                FULL OUTER JOIN predictions_prophet p ON s.date = p.date
                ORDER BY s.date ASC;
            """
            results = execute_query(query)
            if not results:
                return pd.DataFrame()
            
            df = pd.DataFrame(results)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except Exception as e:
            logger.error(f"Error getting combined predictions: {e}")
            raise
    
    @staticmethod
    def get_latest_stock_price(days=30):
        """Get latest stock prices"""
        try:
            query = """
                SELECT date as "Date", close as "Close"
                FROM tesla_stock_data
                ORDER BY date DESC
                LIMIT %s;
            """
            results = execute_query(query, (days,))
            if not results:
                return pd.DataFrame()
            
            df = pd.DataFrame(results)
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')
            return df
        except Exception as e:
            logger.error(f"Error getting latest stock prices: {e}")
            raise
