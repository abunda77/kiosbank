import requests
import time
import json

"""
AUTO-UPDATE IP WHITELIST
Script ini akan:
1. Cek IP publik Anda saat ini
2. Bandingkan dengan IP terakhir yang tersimpan
3. Jika berbeda, update whitelist via API KIOSBANK (jika tersedia)

CATATAN: Ini hanya bisa jalan jika KIOSBANK menyediakan API untuk update whitelist
"""

def get_current_ip():
    """Get current public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return None

def load_last_ip():
    """Load last registered IP from file"""
    try:
        with open('last_registered_ip.txt', 'r') as f:
            return f.read().strip()
    except:
        return None

def save_ip(ip):
    """Save IP to file"""
    with open('last_registered_ip.txt', 'w') as f:
        f.write(ip)

def update_whitelist_api(new_ip):
    """
    Update whitelist via KIOSBANK API
    
    CATATAN: Ini contoh saja. Anda perlu tanya ke KIOSBANK:
    1. Apakah ada API untuk update whitelist?
    2. Apa endpoint dan format request-nya?
    3. Apakah perlu authentication?
    """
    
    # CONTOH (sesuaikan dengan API KIOSBANK yang sebenarnya):
    # url = 'https://development.kiosbank.com/api/whitelist/update'
    # payload = {
    #     'ip_address': new_ip,
    #     'category': 'Development'
    # }
    # response = requests.post(url, json=payload, auth=...)
    
    print(f"⚠️ API update whitelist belum tersedia")
    print(f"   Silakan update manual di dashboard: {new_ip}")
    return False

def check_and_update():
    """Main function to check and update IP"""
    current_ip = get_current_ip()
    last_ip = load_last_ip()
    
    print("="*60)
    print("IP Whitelist Monitor")
    print("="*60)
    print(f"Current IP: {current_ip}")
    print(f"Last Registered IP: {last_ip}")
    
    if current_ip != last_ip:
        print("\n⚠️ IP ADDRESS CHANGED!")
        print(f"   Old IP: {last_ip}")
        print(f"   New IP: {current_ip}")
        print("\n📝 Action Required:")
        print(f"   1. Login to KIOSBANK dashboard")
        print(f"   2. Update whitelist with new IP: {current_ip}")
        print(f"   3. Wait for approval")
        
        # Attempt auto-update (if API available)
        if update_whitelist_api(current_ip):
            print("\n✅ Whitelist updated automatically!")
            save_ip(current_ip)
        else:
            print("\n⚠️ Manual update required in dashboard")
    else:
        print("\n✅ IP unchanged - no action needed")
    
    print("="*60)

if __name__ == "__main__":
    # Run once
    check_and_update()
    
    # Optional: Run continuously (uncomment below)
    # print("\nMonitoring IP changes every 5 minutes...")
    # while True:
    #     check_and_update()
    #     time.sleep(300)  # Check every 5 minutes
