#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import requests
from requests.auth import HTTPDigestAuth
import urllib3
from env_config import get_env, get_env_bool, get_env_int

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================
# KONFIGURASI VPS GATEWAY
# ============================================================

# Load from environment variables
VPS_IP = get_env('VPS_IP', required=True)
VPS_USER = get_env('VPS_USER', required=True)

# Proxy Configuration
USE_PROXY = get_env_bool('USE_PROXY', default=True)
PROXY_HOST = get_env('PROXY_HOST', default='127.0.0.1')
PROXY_PORT = get_env_int('PROXY_PORT', default=1080)

# KIOSBANK API Configuration
API_URL = get_env('KIOSBANK_API_URL', required=True)
API_USERNAME = get_env('KIOSBANK_API_USERNAME', required=True)
API_PASSWORD = get_env('KIOSBANK_API_PASSWORD', required=True)

# Payload
payload = {
    "mitra": get_env('KIOSBANK_MITRA', required=True),
    "accountID": get_env('KIOSBANK_ACCOUNT_ID', required=True),
    "merchantID": get_env('KIOSBANK_MERCHANT_ID', required=True),
    "merchantName": get_env('KIOSBANK_MERCHANT_NAME', required=True),
    "counterID": get_env('KIOSBANK_COUNTER_ID', required=True)
}

# ============================================================
# SETUP PROXY
# ============================================================

proxies = None
if USE_PROXY:
    proxies = {
        'http': f'socks5://{PROXY_HOST}:{PROXY_PORT}',
        'https': f'socks5://{PROXY_HOST}:{PROXY_PORT}'
    }
    print("="*60)
    print("VPS GATEWAY CONFIGURATION")
    print("="*60)
    print(f"VPS IP: {VPS_IP}")
    print(f"VPS User: {VPS_USER}")
    print(f"🔒 Using SOCKS5 proxy: {PROXY_HOST}:{PROXY_PORT}")
    print("="*60)
else:
    print("⚠️  Direct connection (no proxy)")

# ============================================================
# VERIFY PROXY CONNECTION
# ============================================================

if USE_PROXY:
    try:
        print("\n📡 Checking proxy connection...")
        ip_check = requests.get(
            'https://api.ipify.org?format=json',
            proxies=proxies,
            timeout=5
        )
        current_ip = ip_check.json()['ip']
        
        print(f"✅ Proxy working!")
        print(f"   Your outgoing IP: {current_ip}")
        
        if current_ip == VPS_IP:
            print(f"   ✓✓ PERFECT! IP matches VPS IP ({VPS_IP})")
        else:
            print(f"   ⚠️  WARNING: IP doesn't match VPS IP")
            print(f"      Expected: {VPS_IP}")
            print(f"      Got: {current_ip}")
            print(f"      This might be okay if VPS has multiple IPs")
        
        print(f"\n   Make sure this IP ({current_ip}) is whitelisted in KIOSBANK!\n")
        
    except requests.exceptions.ProxyError as e:
        print(f"❌ Proxy connection failed!")
        print("\nTroubleshooting:")
        print("1. Make sure SSH tunnel is running:")
        print(f"   ssh -D 1080 -N {VPS_USER}@{VPS_IP}")
        print("   OR run: start_ssh_tunnel.bat")
        print("\n2. Check if proxy is listening:")
        print("   netstat -ano | findstr 1080")
        print(f"\nError: {str(e)[:200]}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error checking proxy: {str(e)}")
        sys.exit(1)

# ============================================================
# KIOSBANK SIGN-ON REQUEST
# ============================================================

print("="*60)
print("KIOSBANK Sign-On Request")
print("="*60)
print(f"URL: {API_URL}")
print(f"Username: {API_USERNAME}")
print(f"Payload: {payload}")
print("="*60)

try:
    response = requests.post(
        API_URL,
        auth=HTTPDigestAuth(API_USERNAME, API_PASSWORD),
        headers={'Content-Type': 'application/json'},
        json=payload,
        proxies=proxies,
        verify=False,
        timeout=30
    )
    
    print(f"\n✓ Response received!")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            session_id = data.get('SessionID')
            
            print("\n" + "="*60)
            print("✅✅ SIGN-ON SUCCESSFUL!")
            print("="*60)
            print(f"SessionID: {session_id}")
            print("="*60)
            
            # Save session ID to file
            with open('session_id.txt', 'w') as f:
                f.write(session_id)
            print("\n✓ SessionID saved to session_id.txt")
            
            # Save with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('session_history.txt', 'a') as f:
                f.write(f"{timestamp} | {session_id}\n")
            print("✓ SessionID logged to session_history.txt")
            
        except Exception as e:
            print(f"\n⚠️  Warning: Could not parse JSON response")
            print(f"Response: {response.text}")
            
    elif response.status_code == 404:
        print("\n❌ 404 Not Found")
        print("Possible causes:")
        print("1. Endpoint URL incorrect")
        print("2. API not deployed to development server")
        print(f"\nResponse: {response.text[:200]}")
        
    elif response.status_code == 401:
        print("\n❌ 401 Unauthorized")
        print("Possible causes:")
        print("1. Username/password incorrect")
        print("2. Digest authentication failed")
        print(f"\nResponse: {response.text[:200]}")
        
    else:
        print(f"\n❌ Failed with status code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text[:500]}")
        
except requests.exceptions.ProxyError as e:
    print("\n❌ PROXY ERROR")
    print("="*60)
    print("Proxy connection failed!")
    print("\nTroubleshooting:")
    print(f"1. Start SSH tunnel: ssh -D 1080 -N {VPS_USER}@{VPS_IP}")
    print("   OR run: start_ssh_tunnel.bat")
    print("2. Verify proxy running: netstat -ano | findstr 1080")
    print(f"\nError: {str(e)[:200]}")
    
except requests.exceptions.ConnectionError as e:
    print("\n❌ CONNECTION ERROR")
    print("="*60)
    print("Cannot connect to KIOSBANK API")
    print("\nPossible causes:")
    print(f"1. VPS IP ({VPS_IP}) not whitelisted yet in KIOSBANK")
    print("2. API server is down")
    print("3. Network/firewall blocking connection")
    print(f"\nError: {str(e)[:200]}")
    
except requests.exceptions.Timeout:
    print("\n❌ REQUEST TIMEOUT")
    print("Server took too long to respond (>30 seconds)")
    
except Exception as e:
    print(f"\n❌ Unexpected error: {type(e).__name__}")
    print(f"Details: {str(e)[:300]}")

print("\n" + "="*60)
print("NEXT STEPS:")
print("="*60)
if USE_PROXY:
    print(f"1. Make sure VPS IP ({VPS_IP}) is whitelisted in KIOSBANK")
    print("2. Wait for whitelist approval")
    print("3. Run this script again")
else:
    print("1. Enable proxy (USE_PROXY = True)")
    print("2. Start SSH tunnel")
    print("3. Run this script again")
print("="*60)
