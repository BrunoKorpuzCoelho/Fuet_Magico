import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'admin123'

DB_NAME = 'fuet_magico_db'
DB_USER = 'cubix'
DB_PASSWORD = 'cubix123'

try:
    print("🔌 Connecting to PostgreSQL...")
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database='postgres'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL")
    
    print(f"\n🔍 Checking if user '{DB_USER}' exists...")
    cursor.execute(f"SELECT 1 FROM pg_roles WHERE rolname='{DB_USER}'")
    user_exists = cursor.fetchone()
    
    if not user_exists:
        print(f"👤 Creating user '{DB_USER}'...")
        cursor.execute(f"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}'")
        print(f"✅ User '{DB_USER}' created successfully")
    else:
        print(f"ℹ️  User '{DB_USER}' already exists, skipping...")
    
    print(f"\n🔍 Checking if database '{DB_NAME}' exists...")
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
    db_exists = cursor.fetchone()
    
    if not db_exists:
        print(f"🗄️  Creating database '{DB_NAME}'...")
        cursor.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER}")
        print(f"✅ Database '{DB_NAME}' created successfully")
    else:
        print(f"ℹ️  Database '{DB_NAME}' already exists, skipping...")
    
    print(f"\n🔐 Granting privileges to '{DB_USER}'...")
    cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER}")
    print(f"✅ Privileges granted to '{DB_USER}'")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*50)
    print("🎉 Database setup completed successfully!")
    print("="*50)
    print(f"Database: {DB_NAME}")
    print(f"User: {DB_USER}")
    print(f"Password: {DB_PASSWORD}")
    print(f"Host: {POSTGRES_HOST}")
    print(f"Port: {POSTGRES_PORT}")
    print("="*50)
    
except psycopg2.Error as e:
    print(f"\n❌ PostgreSQL Error: {e}")
    print("💡 Tips:")
    print("   - Check if PostgreSQL is running")
    print("   - Verify postgres superuser password")
    print("   - Ensure PostgreSQL is accessible on localhost:5432")
    
except Exception as e:
    print(f"\n❌ Unexpected Error: {e}")
