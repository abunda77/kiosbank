#!/usr/bin/env python3
"""
Database Import Helper for KIOSBANK PPOB
Helps import SQL files in the correct order with validation
"""

import os
import sys
import sqlite3
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}[OK] {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}[ERROR] {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}[WARNING] {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}[INFO] {text}{Colors.ENDC}")

def check_file_exists(filepath):
    """Check if SQL file exists"""
    if not os.path.exists(filepath):
        print_error(f"File not found: {filepath}")
        return False
    return True

def execute_sql_file(db_path, sql_file):
    """Execute SQL file and return success status"""
    try:
        # Read SQL file
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        cursor = conn.cursor()
        
        # Execute SQL
        cursor.executescript(sql_content)
        conn.commit()
        conn.close()
        
        return True, None
    except Exception as e:
        return False, str(e)

def verify_data(db_path):
    """Verify imported data"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM kategori")
        kategori_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sub_kategori")
        sub_kategori_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM produk_ppob")
        produk_count = cursor.fetchone()[0]
        
        conn.close()
        
        print_info(f"Kategori: {kategori_count} records")
        print_info(f"Sub Kategori: {sub_kategori_count} records")
        print_info(f"Produk PPOB: {produk_count} records")
        
        return True
    except Exception as e:
        print_error(f"Verification failed: {e}")
        return False

def main():
    print_header("KIOSBANK PPOB Database Import Helper")
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    db_dir = project_root / "db"
    db_path = db_dir / "ppob.db"
    
    print_info(f"Project root: {project_root}")
    print_info(f"Database path: {db_path}")
    
    # SQL files in correct order
    sql_files = [
        ("structure_table.sql", "Creating database structure"),
        ("sample_data_KATEGORI_SUBKATEGORI.sql", "Importing categories and sub-categories"),
        # ("sample_data_PPOB.sql", "Importing PPOB products"),
        ("sample_data_PULSA_PRABAYAR.sql", "Importing PULSA PRABAYAR products")
        # ("sample_data_PAKET_DATA.sql", "Importing PAKET DATA products"),
        # ("sample_data_GAME.sql", "Importing GAME products")
        # ("sample_data_product.sql", "Importing other products (Game, Pulsa, Paket Data)")
    ]
    
    # Check if all files exist
    print_header("Step 1: Checking SQL Files")
    all_files_exist = True
    for sql_file, _ in sql_files:
        file_path = db_dir / sql_file
        if check_file_exists(file_path):
            print_success(f"Found: {sql_file}")
        else:
            all_files_exist = False
            # sample_data_product.sql is optional
            if sql_file != "sample_data_product.sql":
                print_error(f"Missing required file: {sql_file}")
            else:
                print_warning(f"Optional file not found: {sql_file}")
    
    if not all_files_exist:
        # Check if at least required files exist
        required_files = [f for f, _ in sql_files[:3]]  # First 3 files are required
        required_exist = all(check_file_exists(db_dir / f) for f in required_files)
        if not required_exist:
            print_error("\nMissing required SQL files. Cannot proceed.")
            sys.exit(1)
        else:
            print_warning("\nSome optional files are missing, but will continue with required files.")
    
    # Confirm before proceeding
    print_header("Step 2: Confirmation")
    if db_path.exists():
        print_warning(f"Database already exists: {db_path}")
        response = input(f"{Colors.WARNING}Do you want to recreate the database? This will DELETE all existing data! (yes/no): {Colors.ENDC}")
        if response.lower() != 'yes':
            print_info("Import cancelled by user.")
            sys.exit(0)
        else:
            # Backup existing database
            backup_path = db_path.with_suffix('.db.backup')
            print_info(f"Creating backup: {backup_path}")
            import shutil
            shutil.copy2(db_path, backup_path)
            print_success(f"Backup created: {backup_path}")
    else:
        print_info("Database does not exist. Will create new database.")
        response = input(f"{Colors.OKCYAN}Proceed with import? (yes/no): {Colors.ENDC}")
        if response.lower() != 'yes':
            print_info("Import cancelled by user.")
            sys.exit(0)
    
    # Import SQL files
    print_header("Step 3: Importing SQL Files")
    for sql_file, description in sql_files:
        file_path = db_dir / sql_file
        
        # Skip if file doesn't exist (optional files)
        if not file_path.exists():
            print_warning(f"Skipping: {sql_file} (file not found)")
            continue
        
        print_info(f"{description}...")
        print_info(f"Executing: {sql_file}")
        
        success, error = execute_sql_file(db_path, file_path)
        
        if success:
            print_success(f"Successfully imported: {sql_file}")
        else:
            print_error(f"Failed to import: {sql_file}")
            print_error(f"Error: {error}")
            
            # If this is a required file, stop
            if sql_file != "sample_data_product.sql":
                print_error("\nImport failed. Please check the error above.")
                sys.exit(1)
            else:
                print_warning("Optional file import failed, but continuing...")
    
    # Verify imported data
    print_header("Step 4: Verifying Data")
    if verify_data(db_path):
        print_success("Data verification completed successfully!")
    else:
        print_warning("Data verification encountered issues.")
    
    # Final summary
    print_header("Import Complete!")
    print_success(f"Database created successfully: {db_path}")
    print_info("\nYou can now use the database in your application.")
    print_info("To verify data, you can run SQL queries using:")
    print_info(f"  sqlite3 {db_path}")
    print_info("\nFor more information, see: db/migration_guide.md")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nImport cancelled by user (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
