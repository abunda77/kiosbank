#!/usr/bin/env python3
"""
============================================================
KIOSBANK Sign-On - Direct Connection (No Proxy)
============================================================
Untuk dijalankan LANGSUNG di VPS yang sudah di-whitelist
atau dari komputer dengan IP static yang sudah di-whitelist.

TIDAK MEMERLUKAN PROXY karena IP server sudah di-whitelist.
============================================================
"""

import requests
from requests.auth import HTTPDigestAuth
import urllib3
import sys
from datetime import datetime
import os
from env_config import get_env

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================
# KONFIGURASI
# ============================================================

# KIOSBANK API Configuration - Load from environment variables
API_URL = get_env('KIOSBANK_API_URL', required=True)
API_USERNAME = get_env('KIOSBANK_API_USERNAME', required=True)
API_PASSWORD = get_env('KIOSBANK_API_PASSWORD', required=True)

# Payload - Load from environment variables
payload = {
    "mitra": get_env('KIOSBANK_MITRA', required=True),
    "accountID": get_env('KIOSBANK_ACCOUNT_ID', required=True),
    "merchantID": get_env('KIOSBANK_MERCHANT_ID', required=True),
    "merchantName": get_env('KIOSBANK_MERCHANT_NAME', required=True),
    "counterID": get_env('KIOSBANK_COUNTER_ID', required=True)
}

# ============================================================
# VERIFY CURRENT IP
# ============================================================

def check_current_ip():
    """Cek IP address saat ini"""
    try:
        print("📡 Checking current IP address...")
        ip_check = requests.get('https://api.ipify.org?format=json', timeout=5)
        current_ip = ip_check.json()['ip']
        print(f"✅ Current IP: {current_ip}")
        print(f"   Make sure this IP is whitelisted in KIOSBANK!\n")
        return current_ip
    except Exception as e:
        print(f"⚠️  Could not check IP: {str(e)}\n")
        return None

# ============================================================
# KIOSBANK SIGN-ON
# ============================================================

def kiosbank_signon():
    """
    Melakukan Sign-On ke KIOSBANK API
    Returns: (success: bool, session_id: str or None, error: str or None)
    """
    print("=" * 60)
    print("KIOSBANK Sign-On Request")
    print("=" * 60)
    print(f"URL: {API_URL}")
    print(f"Username: {API_USERNAME}")
    print(f"Payload: {payload}")
    print("=" * 60)
    
    try:
        response = requests.post(
            API_URL,
            auth=HTTPDigestAuth(API_USERNAME, API_PASSWORD),
            headers={'Content-Type': 'application/json'},
            json=payload,
            verify=False,
            timeout=30
        )
        
        print(f"\n✓ Response received!")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                session_id = data.get('SessionID')
                
                print("\n" + "=" * 60)
                print("✅✅ SIGN-ON SUCCESSFUL!")
                print("=" * 60)
                print(f"SessionID: {session_id}")
                print("=" * 60)
                
                # Save session ID to file
                with open('session_id.txt', 'w') as f:
                    f.write(session_id)
                print("\n✓ SessionID saved to session_id.txt")
                
                # Save with timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open('session_history.txt', 'a') as f:
                    f.write(f"{timestamp} | {session_id}\n")
                print("✓ SessionID logged to session_history.txt")
                
                return True, session_id, None
                
            except Exception as e:
                error_msg = f"Could not parse JSON response: {str(e)}"
                print(f"\n⚠️  Warning: {error_msg}")
                print(f"Response: {response.text}")
                return False, None, error_msg
                
        elif response.status_code == 404:
            error_msg = "404 Not Found - Endpoint URL incorrect or API not deployed"
            print(f"\n❌ {error_msg}")
            print(f"Response: {response.text[:200]}")
            return False, None, error_msg
            
        elif response.status_code == 401:
            error_msg = "401 Unauthorized - Username/password incorrect"
            print(f"\n❌ {error_msg}")
            print(f"Response: {response.text[:200]}")
            return False, None, error_msg
            
        else:
            error_msg = f"Failed with status code: {response.status_code}"
            print(f"\n❌ {error_msg}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {response.text[:500]}")
            return False, None, error_msg
            
    except requests.exceptions.ConnectionError as e:
        error_msg = "Connection Error - Cannot connect to KIOSBANK API"
        print("\n❌ CONNECTION ERROR")
        print("=" * 60)
        print("Cannot connect to KIOSBANK API")
        print("\nPossible causes:")
        print("1. Your IP is not whitelisted yet in KIOSBANK")
        print("2. API server is down")
        print("3. Network/firewall blocking connection")
        print(f"\nError: {str(e)[:200]}")
        return False, None, error_msg
        
    except requests.exceptions.Timeout:
        error_msg = "Request timeout - Server took too long to respond"
        print(f"\n❌ {error_msg}")
        return False, None, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error: {type(e).__name__} - {str(e)}"
        print(f"\n❌ {error_msg}")
        return False, None, error_msg

# ============================================================
# MAIN
# ============================================================

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("KIOSBANK Sign-On - Direct Connection (No Proxy)")
    print("=" * 60)
    print()
    
    # Check current IP
    current_ip = check_current_ip()
    
    # Perform sign-on
    success, session_id, error = kiosbank_signon()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ SUCCESS!")
        print("=" * 60)
        print(f"SessionID: {session_id}")
        print("\nYou can now use this SessionID for subsequent API calls.")
    else:
        print("❌ FAILED!")
        print("=" * 60)
        print(f"Error: {error}")
        print("\nPlease check:")
        if current_ip:
            print(f"1. Is IP {current_ip} whitelisted in KIOSBANK?")
        print("2. Are the API credentials correct?")
        print("3. Is the API endpoint URL correct?")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
