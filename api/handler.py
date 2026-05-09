"""Vercel serverless API endpoints untuk TSLA Analytics"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from database import init_pool, close_all_connections
    from data_accessor import DataAccessor
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    print(f"[DEBUG] current_dir: {current_dir}")
    print(f"[DEBUG] parent_dir: {parent_dir}")
    print(f"[DEBUG] sys.path: {sys.path}")
    raise

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database pool on startup
try:
    init_pool()
    logger.info("Database pool initialized for API")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")

@app.before_request
def before_request():
    """Setup for each request"""
    pass

@app.after_request
def after_request(response):
    """Cleanup after each request"""
    return response

# ────────────────────────────────────────────────────────────────────────────
# Root & Info Endpoints
# ────────────────────────────────────────────────────────────────────────────

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - API information"""
    return jsonify({
        "name": "TSLA Analytics API",
        "version": "1.0.0",
        "status": "ready",
        "endpoints": {
            "health": "/api/health",
            "stock_all": "/api/stock/all",
            "stock_by_year": "/api/stock/year/<year>",
            "stock_by_quarter": "/api/stock/year/<year>/quarter/<quarter>",
            "stock_latest": "/api/stock/latest",
            "models_evaluation": "/api/models/evaluation",
            "predictions_sarima": "/api/predictions/sarima",
            "predictions_prophet": "/api/predictions/prophet",
            "predictions_combined": "/api/predictions/combined"
        }
    }), 200

@app.route('/api', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        "name": "TSLA Analytics API",
        "version": "1.0.0",
        "status": "ready"
    }), 200

# ────────────────────────────────────────────────────────────────────────────
# Health & Status Endpoints
# ────────────────────────────────────────────────────────────────────────────

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "TSLA Analytics API"
    }), 200

# ────────────────────────────────────────────────────────────────────────────
# Stock Data Endpoints
# ────────────────────────────────────────────────────────────────────────────

@app.route('/api/stock/all', methods=['GET'])
def get_all_stock_data():
    """Get all Tesla stock data"""
    try:
        df = DataAccessor.get_tesla_stock_data()
        return jsonify({
            "status": "success",
            "data": df.to_dict(orient='records'),
            "count": len(df)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching all stock data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stock/year/<int:year>', methods=['GET'])
def get_stock_by_year(year):
    """Get stock data for specific year"""
    try:
        df = DataAccessor.get_tesla_stock_by_year(year)
        return jsonify({
            "status": "success",
            "year": year,
            "data": df.to_dict(orient='records'),
            "count": len(df)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching stock data for year {year}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stock/year/<int:year>/quarter/<int:quarter>', methods=['GET'])
def get_stock_by_quarter(year, quarter):
    """Get stock data for specific year and quarter"""
    try:
        if quarter not in [1, 2, 3, 4]:
            return jsonify({"status": "error", "message": "Invalid quarter (1-4)"}), 400
        
        df = DataAccessor.get_tesla_stock_by_year_quarter(year, quarter)
        return jsonify({
            "status": "success",
            "year": year,
            "quarter": quarter,
            "data": df.to_dict(orient='records'),
            "count": len(df)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching stock data for {year} Q{quarter}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stock/latest', methods=['GET'])
def get_latest_prices():
    """Get latest stock prices"""
    days = request.args.get('days', 30, type=int)
    try:
        df = DataAccessor.get_latest_stock_price(days)
        return jsonify({
            "status": "success",
            "days": days,
            "data": df.to_dict(orient='records'),
            "count": len(df)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching latest prices: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ────────────────────────────────────────────────────────────────────────────
# Model Evaluation Endpoints
# ────────────────────────────────────────────────────────────────────────────

@app.route('/api/models/evaluation', methods=['GET'])
def get_model_evaluation():
    """Get model evaluation metrics"""
    try:
        df = DataAccessor.get_model_evaluation()
        return jsonify({
            "status": "success",
            "data": df.to_dict(orient='records'),
            "count": len(df)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching model evaluation: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ────────────────────────────────────────────────────────────────────────────
# Prediction Endpoints
# ────────────────────────────────────────────────────────────────────────────

@app.route('/api/predictions/sarima', methods=['GET'])
def get_sarima_predictions():
    """Get SARIMA predictions"""
    try:
        df = DataAccessor.get_predictions_sarima()
        return jsonify({
            "status": "success",
            "model": "SARIMA",
            "data": df.to_dict(orient='records'),
            "count": len(df)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching SARIMA predictions: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/predictions/prophet', methods=['GET'])
def get_prophet_predictions():
    """Get Prophet predictions"""
    try:
        df = DataAccessor.get_predictions_prophet()
        return jsonify({
            "status": "success",
            "model": "Prophet",
            "data": df.to_dict(orient='records'),
            "count": len(df)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching Prophet predictions: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/predictions/combined', methods=['GET'])
def get_combined_predictions():
    """Get predictions from both models"""
    try:
        df = DataAccessor.get_combined_predictions()
        return jsonify({
            "status": "success",
            "models": ["SARIMA", "Prophet"],
            "data": df.to_dict(orient='records'),
            "count": len(df)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching combined predictions: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ────────────────────────────────────────────────────────────────────────────
# Error Handlers
# ────────────────────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "code": 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "status": "error",
        "message": "Internal server error",
        "code": 500
    }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "code": 404,
        "message": "Endpoint not found",
        "status": "error",
        "path": request.path
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {error}")
    return jsonify({
        "code": 500,
        "message": "Internal server error",
        "status": "error"
    }), 500

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)
