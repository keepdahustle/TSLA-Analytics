#!/usr/bin/env python
"""
Setup Supabase PostgreSQL Connection untuk TSLA Analytics
Script ini membantu Anda setup dan test connection ke Supabase
"""

import os
import sys
import logging
from pathlib import Path
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

def parse_database_url(url):
    """Parse PostgreSQL connection URL"""
    try:
        parsed = urlparse(url)
        return {
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path.lstrip('/') or 'postgres',
            'user': parsed.username or 'postgres',
            'password': parsed.password
        }
    except Exception as e:
        logger.error(f"Failed to parse DATABASE_URL: {e}")
        return None

def test_connection(db_config):
    """Test PostgreSQL connection"""
    try:
        import psycopg2
        
        logger.info(f"Testing connection to {db_config['host']}:{db_config['port']}...")
        
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            connect_timeout=10
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        logger.info("✓ Connection successful!")
        logger.info(f"  PostgreSQL Version: {version.split(',')[0]}")
        
        # Get database stats
        cursor.execute("""
            SELECT 
                COUNT(*) as tables_count
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables_count = cursor.fetchone()[0]
        logger.info(f"  Tables found: {tables_count}")
        
        # List tables
        if tables_count > 0:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = cursor.fetchall()
            logger.info("  Tables:")
            for table in tables:
                # Get row count
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                logger.info(f"    - {table_name}: {row_count} rows")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        logger.error("psycopg2 not installed. Run: pip install psycopg2-binary")
        return False
    except Exception as e:
        logger.error(f"✗ Connection failed: {e}")
        return False

def create_env_file(database_url):
    """Create .env file dari template"""
    try:
        script_dir = Path(__file__).parent
        template_path = script_dir / '.env.supabase.template'
        env_path = script_dir / '.env'
        
        if not template_path.exists():
            logger.error(f"Template file not found: {template_path}")
            return False
        
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace placeholder
        content = content.replace('DATABASE_URL=', f'DATABASE_URL={database_url}')
        
        # Write .env
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✓ Created .env file")
        logger.info(f"  Location: {env_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create .env file: {e}")
        return False

def get_database_url():
    """Get DATABASE_URL from user input or environment"""
    # Check if already in environment
    if os.getenv('DATABASE_URL'):
        logger.info(f"Found DATABASE_URL in environment")
        return os.getenv('DATABASE_URL')
    
    # Prompt user
    print("\n" + "="*70)
    print("SUPABASE DATABASE CONNECTION SETUP")
    print("="*70)
    print("\nCara mendapatkan DATABASE_URL:")
    print("1. Buka https://supabase.com/dashboard")
    print("2. Pilih project: 'tsla-analytics'")
    print("3. Sidebar → 'Project Settings'")
    print("4. Tab → 'Database'")
    print("5. Copy Connection String (gunakan URI tab)")
    print("\nGunakan format Pooling untuk Vercel:")
    print("  postgresql://postgres.[ref]:[password]@aws-0-[region].pooling.supabase.com:6543/postgres")
    print("\nAtau format Direct:")
    print("  postgresql://postgres:[password]@[host].supabase.co:5432/postgres")
    print("="*70)
    
    database_url = input("\nPaste DATABASE_URL: ").strip()
    
    if not database_url:
        logger.error("DATABASE_URL tidak boleh kosong")
        return None
    
    if not database_url.startswith('postgresql://'):
        logger.error("DATABASE_URL harus dimulai dengan 'postgresql://'")
        return None
    
    return database_url

def main():
    """Main setup function"""
    print("\n" + "="*70)
    print("🚀 TSLA Analytics - Supabase PostgreSQL Setup")
    print("="*70)
    
    # Get DATABASE_URL
    database_url = get_database_url()
    if not database_url:
        logger.error("Setup dibatalkan")
        return False
    
    # Parse connection details
    db_config = parse_database_url(database_url)
    if not db_config:
        logger.error("Setup dibatalkan")
        return False
    
    logger.info("\nConnection Details:")
    logger.info(f"  Host: {db_config['host']}")
    logger.info(f"  Port: {db_config['port']}")
    logger.info(f"  Database: {db_config['database']}")
    logger.info(f"  User: {db_config['user']}")
    
    # Test connection
    print("\n" + "-"*70)
    if not test_connection(db_config):
        logger.error("\nSetup dibatalkan - Connection gagal")
        print("\nTroubleshooting:")
        print("  1. Verifikasi DATABASE_URL benar")
        print("  2. Check password tidak ada typo")
        print("  3. Pastikan Supabase project sudah aktif")
        print("  4. Cek firewall/network")
        return False
    
    # Create .env file
    print("\n" + "-"*70)
    if not create_env_file(database_url):
        logger.error("Setup dibatalkan - Gagal create .env")
        return False
    
    # Success
    print("\n" + "="*70)
    logger.info("✓ SETUP BERHASIL!")
    print("="*70)
    print("\nLangkah selanjutnya:")
    print("  1. File .env sudah dibuat dengan DATABASE_URL")
    print("  2. (Optional) Update setup.py untuk load data ke Supabase:")
    print("     python setup.py")
    print("  3. Deploy ke Vercel:")
    print("     vercel --prod")
    print("\nUntuk Vercel environment variables:")
    print("  1. Buka https://vercel.com/dashboard")
    print("  2. Project Settings → Environment Variables")
    print("  3. Add DATABASE_URL dengan value dari .env")
    print("\n" + "="*70 + "\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
