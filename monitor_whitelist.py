import requests
from requests.auth import HTTPDigestAuth
import urllib3
import time
from datetime import datetime
from env_config import get_env, get_env_int

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================
# KONFIGURASI
# ============================================================

# Load from environment variables
VPS_IP = get_env('VPS_IP', required=True)
PROXY_HOST = get_env('PROXY_HOST', default='127.0.0.1')
PROXY_PORT = get_env_int('PROXY_PORT', default=1080)

API_URL = get_env('KIOSBANK_API_URL', required=True)
API_USERNAME = get_env('KIOSBANK_API_USERNAME', required=True)
API_PASSWORD = get_env('KIOSBANK_API_PASSWORD', required=True)

payload = {
    "mitra": get_env('KIOSBANK_MITRA', required=True),
    "accountID": get_env('KIOSBANK_ACCOUNT_ID', required=True),
    "merchantID": get_env('KIOSBANK_MERCHANT_ID', required=True),
    "merchantName": get_env('KIOSBANK_MERCHANT_NAME', required=True),
    "counterID": get_env('KIOSBANK_COUNTER_ID', required=True)
}

proxies = {
    'http': f'socks5://{PROXY_HOST}:{PROXY_PORT}',
    'https': f'socks5://{PROXY_HOST}:{PROXY_PORT}'
}

# ============================================================
# MONITORING FUNCTION
# ============================================================

def test_connection():
    """Test connection to KIOSBANK API"""
    try:
        response = requests.post(
            API_URL,
            auth=HTTPDigestAuth(API_USERNAME, API_PASSWORD),
            headers={'Content-Type': 'application/json'},
            json=payload,
            proxies=proxies,
            verify=False,
            timeout=10
        )
        return response.status_code, response.text
    except requests.exceptions.ConnectionError as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)

def monitor_whitelist(interval_seconds=60, max_attempts=None):
    """
    Monitor whitelist status by testing API connection
    
    Args:
        interval_seconds: Time between checks (default: 60 seconds)
        max_attempts: Maximum number of attempts (None = infinite)
    """
    print("="*60)
    print("KIOSBANK WHITELIST MONITOR")
    print("="*60)
    print(f"VPS IP: {VPS_IP}")
    print(f"Monitoring interval: {interval_seconds} seconds")
    print(f"Press Ctrl+C to stop")
    print("="*60)
    
    # Verify proxy first
    try:
        ip_check = requests.get(
            'https://api.ipify.org?format=json',
            proxies=proxies,
            timeout=5
        )
        current_ip = ip_check.json()['ip']
        print(f"\n✅ Proxy working! Outgoing IP: {current_ip}")
        
        if current_ip != VPS_IP:
            print(f"⚠️  WARNING: IP mismatch!")
            print(f"   Expected: {VPS_IP}")
            print(f"   Got: {current_ip}")
    except Exception as e:
        print(f"\n❌ Proxy error: {e}")
        print("Make sure SSH tunnel is running!")
        return
    
    print("\n" + "="*60)
    print("Starting monitoring...")
    print("="*60 + "\n")
    
    attempt = 0
    while True:
        attempt += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if max_attempts and attempt > max_attempts:
            print(f"\n[{timestamp}] Reached maximum attempts ({max_attempts})")
            break
        
        print(f"[{timestamp}] Attempt #{attempt}: Testing connection...", end=" ")
        
        status_code, response = test_connection()
        
        if status_code == 200:
            print("✅ SUCCESS!")
            print("\n" + "="*60)
            print("🎉 WHITELIST APPROVED!")
            print("="*60)
            print(f"Response: {response}")
            
            try:
                import json
                data = json.loads(response)
                session_id = data.get('SessionID')
                print(f"\nSessionID: {session_id}")
                
                # Save session ID
                with open('session_id.txt', 'w') as f:
                    f.write(session_id)
                print("✓ SessionID saved to session_id.txt")
            except:
                pass
            
            print("\n✅ You can now use KIOSBANK API!")
            break
            
        elif status_code == 404:
            print("❌ 404 - Endpoint not found")
            print(f"   Response: {response[:100]}")
            
        elif status_code == 401:
            print("❌ 401 - Authentication failed")
            print(f"   Response: {response[:100]}")
            
        elif status_code:
            print(f"❌ Status {status_code}")
            print(f"   Response: {response[:100]}")
            
        else:
            # Connection error (likely not whitelisted yet)
            print("⏳ Not whitelisted yet")
            if "Max retries" in response or "Connection" in response:
                print("   → IP still not in whitelist")
            else:
                print(f"   → {response[:80]}")
        
        # Wait before next attempt
        if max_attempts is None or attempt < max_attempts:
            print(f"   Waiting {interval_seconds} seconds before next check...\n")
            try:
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                print("\n\n" + "="*60)
                print("Monitoring stopped by user")
                print("="*60)
                break

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("KIOSBANK IP WHITELIST MONITORING TOOL")
    print("="*60)
    print("\nThis tool will continuously check if your VPS IP")
    print("has been whitelisted by testing the KIOSBANK API.")
    print("\nOptions:")
    print("1. Monitor every 60 seconds (recommended)")
    print("2. Monitor every 5 minutes")
    print("3. Test once only")
    print("4. Custom interval")
    print("\nPress Ctrl+C anytime to stop")
    print("="*60)
    
    try:
        choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"
        
        if choice == "1":
            monitor_whitelist(interval_seconds=60)
        elif choice == "2":
            monitor_whitelist(interval_seconds=300)
        elif choice == "3":
            monitor_whitelist(interval_seconds=1, max_attempts=1)
        elif choice == "4":
            interval = int(input("Enter interval in seconds: "))
            monitor_whitelist(interval_seconds=interval)
        else:
            print("Invalid choice. Using default (60 seconds)")
            monitor_whitelist(interval_seconds=60)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring cancelled by user")
    except Exception as e:
        print(f"\nError: {e}")
