# TSLA Analytics

## Overview
Aplikasi ini adalah Tesla Stock Analysis Dashboard yang menggunakan PostgreSQL sebagai database backend, bukan CSV lokal. Structure ini dioptimalkan untuk deployment di Vercel dengan serverless functions.

## Prerequisites
- PostgreSQL database (hosted pada platform seperti AWS RDS, Neon, Render, atau platform lainnya)
- Vercel account
- Git repository
- Python 3.9+

## Project Structure

```
Deploy/
├── api/
│   ├── __init__.py           # API package initialization
│   └── handler.py            # Vercel serverless function - Flask app
├── migrations/
│   └── 001_init_schema.py    # Database schema creation
├── config.py                 # Configuration management
├── database.py               # Database connection pool & utilities
├── data_accessor.py          # Data access layer (replaces CSV reading)
├── data_loader.py            # CSV to PostgreSQL data loader
├── dashboard.py              # Dash dashboard (local development)
├── setup.py                  # Database initialization script
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel configuration
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Installation & Setup

### 1. Clone Repository dan Setup Local Environment

```bash
cd Deploy
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Setup Database

#### Option A: PostgreSQL Lokal (untuk development)

```bash
# Create database
createdb tesla_stock

# Copy environment template
copy .env.example .env

# Edit .env dengan database credentials
# DATABASE_URL=postgresql://username:password@localhost:5432/tesla_stock
```

#### Option B: Remote PostgreSQL (untuk production)

Pilih salah satu platform:

**Neon (Recommended)**
- Daftar di https://neon.tech
- Create project dan copy DATABASE_URL
- Format: `postgresql://user:password@endpoint.neon.tech:5432/tesla_stock`

**AWS RDS**
- Create RDS PostgreSQL instance
- Format: `postgresql://user:password@endpoint.rds.amazonaws.com:5432/tesla_stock`

**Render**
- Daftar di https://render.com
- Create PostgreSQL database
- Copy connection string

**Railway**
- Daftar di https://railway.app
- Create PostgreSQL service
- Copy DATABASE_URL

### 3. Initialize Database & Load Data

```bash
# Pastikan CSV files ada di parent directory atau current directory:
# - Tesla_stock_data.csv
# - model_evaluation.csv
# - predictions_sarima.csv
# - predictions_prophet.csv

# Run setup script
python setup.py

# Output yang diharapkan:
# [INFO] Starting database setup...
# [INFO] Found Tesla_stock_data.csv in parent directory
# [INFO] Creating database tables...
# [INFO] Loading data from CSV files...
# [INFO] ✓ Database setup completed successfully!
```

### 4. Test API Lokal

```bash
# Terminal 1: Run Flask API
python -m flask --app api.handler run

# Output:
# * Running on http://127.0.0.1:5000
# * Press CTRL+C to quit

# Terminal 2: Test endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/stock/latest
curl http://localhost:5000/api/models/evaluation
```

### 5. Test Dashboard Lokal (Optional)

```bash
python dashboard.py
# Buka http://localhost:8050 di browser
```

## Deployment ke Vercel

### Step 1: Prepare Git Repository

```bash
# Jika belum git repository
git init
git add .
git commit -m "Initial commit - TSLA Analytics for Vercel"
git branch -M main

# Push ke GitHub/GitLab
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

### Step 2: Connect ke Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login ke Vercel
vercel login

# Deploy
vercel
```

Atau langsung via Vercel Dashboard:
1. Buka https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import repository GitHub
4. Configure project
5. Add environment variables (lihat step 3)

### Step 3: Add Environment Variables

Di Vercel Dashboard, go to Project Settings → Environment Variables:

Add:
```
DATABASE_URL = postgresql://user:password@host:port/dbname
FLASK_ENV = production
```

### Step 4: Initialize Database (First Deployment Only)

```bash
# Option 1: Via Vercel CLI
vercel env pull .env.local
# Pastikan CSV files tersedia

# Option 2: Connect via SSH/Vercel CLI dan run setup
vercel ssh
python setup.py
```

Atau upload CSV files terlebih dahulu menggunakan tools seperti:
- pgAdmin web interface
- DBeaver
- psql command line

### Step 5: Verify Deployment

```bash
# Check deployment status
vercel ls

# Test API endpoints
curl https://your-project.vercel.app/api/health
curl https://your-project.vercel.app/api/stock/latest
```

## API Endpoints

### Health Check
```
GET /api/health
```

### Stock Data
```
GET /api/stock/all                              # Get all stock data
GET /api/stock/year/2024                        # Get data for specific year
GET /api/stock/year/2024/quarter/1              # Get data for specific quarter
GET /api/stock/latest?days=30                   # Get latest prices
```

### Model Evaluation
```
GET /api/models/evaluation                      # Get all model metrics
```

### Predictions
```
GET /api/predictions/sarima                     # Get SARIMA predictions
GET /api/predictions/prophet                    # Get Prophet predictions
GET /api/predictions/combined                   # Get combined predictions
```

### Response Format
```json
{
  "status": "success",
  "data": [...],
  "count": 100
}
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://user:pass@host:5432/db |
| DB_HOST | Database hostname | localhost |
| DB_PORT | Database port | 5432 |
| DB_NAME | Database name | tesla_stock |
| DB_USER | Database user | postgres |
| DB_PASSWORD | Database password | secret123 |
| FLASK_ENV | Flask environment | production |
| DEBUG | Debug mode | false |

## Database Schema

### tesla_stock_data
```sql
- id (SERIAL PRIMARY KEY)
- date (DATE UNIQUE)
- close (FLOAT)
- high (FLOAT)
- low (FLOAT)
- open (FLOAT)
- volume (BIGINT)
- year (INT)
- quarter (INT)
- month (INT)
- created_at (TIMESTAMP)
```

### model_evaluation
```sql
- id (SERIAL PRIMARY KEY)
- model (VARCHAR UNIQUE)
- mae (FLOAT)
- rmse (FLOAT)
- mape_percentage (FLOAT)
- r_squared (FLOAT)
- dir_accuracy (FLOAT)
- dir_precision (FLOAT)
- dir_recall (FLOAT)
- dir_f1 (FLOAT)
- created_at (TIMESTAMP)
```

### predictions_sarima
```sql
- id (SERIAL PRIMARY KEY)
- date (DATE UNIQUE)
- actual (FLOAT)
- sarima_pred (FLOAT)
- created_at (TIMESTAMP)
```

### predictions_prophet
```sql
- id (SERIAL PRIMARY KEY)
- date (DATE UNIQUE)
- actual (FLOAT)
- prophet_pred (FLOAT)
- created_at (TIMESTAMP)
```

## Troubleshooting

### Database Connection Error
```
Error: "could not connect to server"
```
- Verify DATABASE_URL is correct
- Check if database is running
- Check firewall/security groups allow connection

### CSV Files Not Found
```
Error: "Missing CSV files"
```
- Pastikan CSV files ada di parent directory Deploy folder
- Atau copy CSV files ke Deploy directory
- Update path di setup.py jika perlu

### Memory Issues
```
Error: "Lambda layers must be less than 15MB"
```
- Reduce dependencies atau split into separate layers
- Remove unused packages dari requirements.txt

### Slow Queries
- Add indexes: Modify migrations/001_init_schema.py
- Optimize queries di data_accessor.py
- Consider connection pooling adjustments

### Import Errors
```
ModuleNotFoundError: No module named 'database'
```
- Pastikan venv teractivate
- Re-install requirements: `pip install -r requirements.txt`
- Check sys.path di handler.py

## Local Development

### Run API Server
```bash
python -m flask --app api.handler run
```

### Run Dashboard
```bash
python dashboard.py
```

### Run Tests
```bash
# Setup pytest
pip install pytest pytest-flask

# Run tests
pytest
```

### Database Migrations
Edit `migrations/001_init_schema.py` dan run:
```bash
python -c "from migrations.init_schema import create_tables; create_tables()"
```

## Security Best Practices

1. **Never commit .env file**
   - Already in .gitignore
   - Use .env.example sebagai template

2. **Database Security**
   - Use strong passwords
   - Restrict database access by IP
   - Use SSL connections

3. **API Security**
   - Add rate limiting
   - Implement authentication
   - Use CORS properly

4. **Secrets Management**
   - Use Vercel's environment variables
   - Never hardcode secrets
   - Rotate credentials periodically

## Performance Optimization

1. **Connection Pooling**: Sudah implemented di database.py
2. **Query Optimization**: Gunakan indexes, limit results
3. **Caching**: Consider implementing Redis
4. **Pagination**: Implement untuk large datasets

## Monitoring & Logging

1. **Vercel Logs**
   ```bash
   vercel logs
   ```

2. **Application Logs**
   - Check logs di Vercel dashboard
   - Configure CloudWatch (jika AWS RDS)

3. **Database Monitoring**
   - Monitor connections
   - Watch query performance
   - Setup alerts

## Updates & Maintenance

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
# Vercel akan auto-redeploy
```

### Database Maintenance
```bash
# Backup database
pg_dump $DATABASE_URL > backup.sql

# Restore from backup
psql $DATABASE_URL < backup.sql
```

## Support & Documentation

- Flask: https://flask.palletsprojects.com
- Vercel Python: https://vercel.com/docs/functions/python
- PostgreSQL: https://www.postgresql.org/docs/
- Psycopg2: https://www.psycopg.org/documentation/
- Dash: https://dash.plotly.com

## License
MIT License

## Contact
For issues or questions, create an issue on GitHub repository.
