Deploy/
│
├── 📁 api/
│   ├── __init__.py                 # API package init
│   └── handler.py                  # Flask Vercel serverless function
│                                   # - GET /api/health
│                                   # - GET /api/stock/all, year, quarter, latest
│                                   # - GET /api/models/evaluation
│                                   # - GET /api/predictions/sarima, prophet, combined
│
├── 📁 migrations/
│   ├── __init__.py                 # Migrations package init
│   └── 001_init_schema.py          # Create database tables & indexes
│
├── config.py                        # Configuration management
│                                   # - PostgreSQL connection settings
│                                   # - Flask configuration
│                                   # - Connection pool settings
│
├── database.py                      # Database layer
│                                   # - Connection pooling (SimpleConnectionPool)
│                                   # - Query execution helpers
│                                   # - Batch operations
│
├── data_accessor.py                 # Data access layer
│                                   # - Replaces CSV reading
│                                   # - get_tesla_stock_data()
│                                   # - get_model_evaluation()
│                                   # - get_predictions_*()
│
├── data_loader.py                   # CSV to PostgreSQL loader
│                                   # - load_tesla_stock_data()
│                                   # - load_model_evaluation()
│                                   # - load_predictions_sarima()
│                                   # - load_predictions_prophet()
│                                   # - initialize_database()
│
├── dashboard.py                     # Modified Dash dashboard
│                                   # - Uses PostgreSQL instead of CSV
│                                   # - Same UI/UX as original
│
├── setup.py                         # Database initialization script
│                                   # - Create tables
│                                   # - Load CSV data to PostgreSQL
│                                   # - Usage: python setup.py
│
├── test_api.py                      # API endpoint testing script
│                                   # - Test all endpoints
│                                   # - Usage: python test_api.py
│
├── __init__.py                      # Package initialization
│
├── requirements.txt                 # Python dependencies
│                                   # - Flask, psycopg2, pandas, plotly, dash
│                                   # - Compatible with Vercel
│
├── vercel.json                      # Vercel configuration
│                                   # - Builds: Python 3.9
│                                   # - Routes: /api/* → handler.py
│                                   # - Environment variables
│
├── .env.example                     # Environment template
│                                   # - DATABASE_URL
│                                   # - DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
│
├── .gitignore                       # Git ignore rules
│                                   # - .env files
│                                   # - venv/
│                                   # - __pycache__/
│                                   # - Database files
│
├── README.md                        # Main documentation
│                                   # - Overview
│                                   # - Installation & setup
│                                   # - Local development
│                                   # - Vercel deployment steps
│                                   # - Troubleshooting
│                                   # - Security best practices
│
├── API_DOCUMENTATION.md             # Complete API reference
│                                   # - All endpoints
│                                   # - Request/response examples
│                                   # - Error codes
│                                   # - Integration examples
│
└── DEPLOYMENT_CHECKLIST.md          # Quick deployment guide
                                    # - Pre-deployment checklist
                                    # - Vercel deployment steps
                                    # - Post-deployment verification
                                    # - Troubleshooting quick tips

═══════════════════════════════════════════════════════════════════════════════

## Key Features

✓ PostgreSQL Integration
  - Connection pooling for efficiency
  - Automatic indexes on date columns
  - Transaction support

✓ CSV to Database Migration
  - Automatic data type conversion
  - Date parsing & year/quarter/month extraction
  - Batch insert for performance

✓ REST API (Vercel Serverless)
  - 10+ endpoints
  - Stock data queries
  - Model predictions comparison
  - Performance metrics

✓ Production Ready
  - Error handling
  - Logging
  - CORS support
  - Environment configuration
  - Connection pooling

✓ Easy Deployment
  - Single-command setup
  - Vercel.json pre-configured
  - Environment variable template
  - Deployment checklist included

═══════════════════════════════════════════════════════════════════════════════

## Quick Start

1. Setup environment:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your PostgreSQL URL
   ```

2. Initialize database:
   ```bash
   python setup.py
   ```

3. Test API:
   ```bash
   python -m flask --app api.handler run
   # In another terminal:
   python test_api.py
   ```

4. Deploy to Vercel:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   # Connect to Vercel and deploy
   ```

═══════════════════════════════════════════════════════════════════════════════

## Database Schema

### tesla_stock_data (3922 rows)
- date, close, high, low, open, volume
- year, quarter, month (derived)
- Indexed on date

### model_evaluation (2 rows)
- Model: SARIMA, Prophet
- Metrics: MAE, RMSE, MAPE, R², Dir Accuracy, etc.

### predictions_sarima (61 rows)
- date, actual, sarima_pred
- Indexed on date

### predictions_prophet (61 rows)
- date, actual, prophet_pred
- Indexed on date

═══════════════════════════════════════════════════════════════════════════════

## API Endpoints

GET /api/health
GET /api/stock/all
GET /api/stock/year/{year}
GET /api/stock/year/{year}/quarter/{quarter}
GET /api/stock/latest?days=30
GET /api/models/evaluation
GET /api/predictions/sarima
GET /api/predictions/prophet
GET /api/predictions/combined

═══════════════════════════════════════════════════════════════════════════════

## Technology Stack

- Backend: Flask + Python 3.9
- Database: PostgreSQL
- Deployment: Vercel (Serverless)
- API Format: REST/JSON
- Data Visualization: Plotly + Dash (optional local)

═══════════════════════════════════════════════════════════════════════════════

## Notes

- All CSV files are converted to PostgreSQL on setup
- No local CSV files needed after setup
- Connection pooling optimizes database usage
- Vercel handles auto-scaling
- Free tier available for small projects
- PostgreSQL free options: Neon, Render, Railway

═══════════════════════════════════════════════════════════════════════════════
