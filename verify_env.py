#!/usr/bin/env python3
"""
Environment Variables Verification Script
Verifies that all required environment variables are properly configured
"""

import sys
from pathlib import Path
from env_config import get_env, get_env_bool, get_env_int

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def check_env_file_exists():
    """Check if .env file exists"""
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        print("❌ .env file not found!")
        print("\nPlease create .env file:")
        print("  1. Copy .env.example to .env")
        print("  2. Fill in your actual credentials")
        print("\nCommand:")
        print("  cp .env.example .env")
        return False
    print("✅ .env file exists")
    return True

def verify_required_vars():
    """Verify all required environment variables"""
    print_header("Verifying Required Environment Variables")
    
    required_vars = {
        'KIOSBANK_API_URL': 'KIOSBANK API URL',
        'KIOSBANK_API_USERNAME': 'KIOSBANK API Username',
        'KIOSBANK_API_PASSWORD': 'KIOSBANK API Password',
        'KIOSBANK_MITRA': 'KIOSBANK Mitra',
        'KIOSBANK_ACCOUNT_ID': 'KIOSBANK Account ID',
        'KIOSBANK_MERCHANT_ID': 'KIOSBANK Merchant ID',
        'KIOSBANK_MERCHANT_NAME': 'KIOSBANK Merchant Name',
        'KIOSBANK_COUNTER_ID': 'KIOSBANK Counter ID',
        'VPS_IP': 'VPS IP Address',
        'VPS_USER': 'VPS Username',
        'REGISTERED_IP': 'Registered IP in KIOSBANK Dashboard'
    }
    
    all_ok = True
    for var_name, description in required_vars.items():
        try:
            value = get_env(var_name, required=True)
            # Mask sensitive values
            if 'PASSWORD' in var_name or 'SECRET' in var_name:
                display_value = '*' * len(value)
            elif len(value) > 30:
                display_value = value[:27] + '...'
            else:
                display_value = value
            
            print(f"✅ {description:40} = {display_value}")
        except ValueError as e:
            print(f"❌ {description:40} = NOT SET")
            all_ok = False
    
    return all_ok

def verify_optional_vars():
    """Verify optional environment variables"""
    print_header("Verifying Optional Environment Variables")
    
    optional_vars = {
        'VPS_SSH_PORT': ('VPS SSH Port', 22),
        'USE_PROXY': ('Use Proxy', True),
        'PROXY_HOST': ('Proxy Host', '127.0.0.1'),
        'PROXY_PORT': ('Proxy Port', 1080)
    }
    
    for var_name, (description, default) in optional_vars.items():
        if isinstance(default, bool):
            value = get_env_bool(var_name, default=default)
        elif isinstance(default, int):
            value = get_env_int(var_name, default=default)
        else:
            value = get_env(var_name, default=default)
        
        print(f"✅ {description:40} = {value}")

def check_placeholder_values():
    """Check if any values are still placeholders"""
    print_header("Checking for Placeholder Values")
    
    placeholders = [
        'your_username_here',
        'your_password_here',
        'your_account_id_here',
        'your_merchant_id_here',
        'your_merchant_name_here',
        'your_vps_ip_here',
        'your_vps_username_here',
        'your_registered_ip_here'
    ]
    
    all_vars = {
        'KIOSBANK_API_USERNAME': get_env('KIOSBANK_API_USERNAME', default=''),
        'KIOSBANK_API_PASSWORD': get_env('KIOSBANK_API_PASSWORD', default=''),
        'KIOSBANK_ACCOUNT_ID': get_env('KIOSBANK_ACCOUNT_ID', default=''),
        'KIOSBANK_MERCHANT_ID': get_env('KIOSBANK_MERCHANT_ID', default=''),
        'KIOSBANK_MERCHANT_NAME': get_env('KIOSBANK_MERCHANT_NAME', default=''),
        'VPS_IP': get_env('VPS_IP', default=''),
        'VPS_USER': get_env('VPS_USER', default=''),
        'REGISTERED_IP': get_env('REGISTERED_IP', default='')
    }
    
    has_placeholders = False
    for var_name, value in all_vars.items():
        if value.lower() in placeholders:
            print(f"⚠️  {var_name} still has placeholder value: {value}")
            has_placeholders = True
    
    if not has_placeholders:
        print("✅ No placeholder values found")
    
    return not has_placeholders

def verify_gitignore():
    """Verify .gitignore is properly configured"""
    print_header("Verifying .gitignore Configuration")
    
    gitignore_path = Path(__file__).parent / '.gitignore'
    if not gitignore_path.exists():
        print("⚠️  .gitignore file not found")
        return False
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_entries = ['.env', 'session_id.txt', 'session_history.txt']
    all_ok = True
    
    for entry in required_entries:
        if entry in content:
            print(f"✅ .gitignore contains: {entry}")
        else:
            print(f"❌ .gitignore missing: {entry}")
            all_ok = False
    
    return all_ok

def main():
    """Main verification function"""
    print("\n" + "=" * 60)
    print("KIOSBANK Environment Configuration Verification")
    print("=" * 60)
    
    # Check .env file exists
    if not check_env_file_exists():
        sys.exit(1)
    
    # Verify required variables
    required_ok = verify_required_vars()
    
    # Verify optional variables
    verify_optional_vars()
    
    # Check for placeholders
    no_placeholders = check_placeholder_values()
    
    # Verify .gitignore
    gitignore_ok = verify_gitignore()
    
    # Final summary
    print_header("Verification Summary")
    
    if required_ok and no_placeholders and gitignore_ok:
        print("✅ All checks passed!")
        print("\nYour environment is properly configured.")
        print("You can now run the KIOSBANK scripts.")
        print("\nNext steps:")
        print("  1. python check_ip.py          - Check your current IP")
        print("  2. python start_ssh_tunnel.py  - Start SSH tunnel (if using proxy)")
        print("  3. python signon_vps.py        - Sign-on to KIOSBANK API")
        return 0
    else:
        print("❌ Some checks failed!")
        print("\nPlease fix the issues above before running the scripts.")
        if not required_ok:
            print("\n⚠️  Missing required environment variables")
            print("   Edit your .env file and add the missing values")
        if not no_placeholders:
            print("\n⚠️  Placeholder values detected")
            print("   Replace placeholder values with your actual credentials")
        if not gitignore_ok:
            print("\n⚠️  .gitignore not properly configured")
            print("   Make sure .env is in .gitignore to prevent credential exposure")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print("\n" + "=" * 60)
    sys.exit(exit_code)
