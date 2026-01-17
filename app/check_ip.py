#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import requests
from env_config import get_env

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("="*60)
print("Checking Your Current Public IP Address")
print("="*60)

try:
    # Method 1: ipify
    response = requests.get('https://api.ipify.org?format=json', timeout=5)
    ip1 = response.json()['ip']
    print(f"\nMethod 1 (ipify): {ip1}")
except:
    ip1 = "Failed"
    print(f"\nMethod 1 (ipify): Failed")

try:
    # Method 2: ip-api
    response = requests.get('http://ip-api.com/json/', timeout=5)
    data = response.json()
    ip2 = data['query']
    print(f"Method 2 (ip-api): {ip2}")
    print(f"  Location: {data.get('city')}, {data.get('country')}")
    print(f"  ISP: {data.get('isp')}")
except:
    ip2 = "Failed"
    print(f"Method 2 (ip-api): Failed")

print("\n" + "="*60)
print("IP Whitelist Verification")
print("="*60)

# Load registered IP from environment variable
registered_ip = get_env('REGISTERED_IP', required=True)
print(f"Registered IP in Dashboard: {registered_ip}")

if ip1 == registered_ip or ip2 == registered_ip:
    print(f"Current IP: {ip1 if ip1 == registered_ip else ip2}")
    print("\n✅ MATCH! Your current IP matches the registered IP.")
    print("   You can proceed once the approval is granted.")
else:
    print(f"Current IP: {ip1 if ip1 != 'Failed' else ip2}")
    print("\n⚠️ WARNING! Your current IP does NOT match!")
    print("   Possible reasons:")
    print("   1. Your IP changed (dynamic IP from ISP)")
    print("   2. You registered a different device's IP")
    print("   3. You're behind a different network now")
    print("\n   Action: Update the whitelist with your current IP")

print("="*60)
