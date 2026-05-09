"""TSLA Analytics - Vercel Deployment Package

This package contains:
- API endpoints for stock data, predictions, and model metrics
- PostgreSQL database layer with connection pooling
- Data access layer abstracting CSV/DB operations
- Migration scripts for database initialization
- Configuration management for different environments
"""

__version__ = "1.0.0"
__author__ = "TSLA Analytics Team"
__description__ = "Tesla Stock Analysis Dashboard - Vercel Ready"

from database import init_pool, close_all_connections, get_connection
from data_accessor import DataAccessor

__all__ = [
    'init_pool',
    'close_all_connections',
    'get_connection',
    'DataAccessor',
]
