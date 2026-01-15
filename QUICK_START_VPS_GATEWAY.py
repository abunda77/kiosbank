# ============================================================
# QUICK START GUIDE: VPS GATEWAY UNTUK KIOSBANK API
# ============================================================

"""
PILIH SOLUSI YANG COCOK:
========================

┌─────────────────────────────────────────────────────────────┐
│ REKOMENDASI BERDASARKAN KEBUTUHAN:                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 🚀 UNTUK TESTING/DEVELOPMENT (Start Here):                 │
│    → SSH SOCKS5 Proxy                                       │
│    ✅ Setup: 5 menit                                        │
│    ✅ Tidak perlu install apapun                            │
│    ✅ Langsung bisa pakai                                   │
│                                                             │
│ 🏭 UNTUK PRODUCTION/HIGH-TRAFFIC:                          │
│    → Shadowsocks                                            │
│    ✅ Lebih cepat & stabil                                  │
│    ✅ Auto-reconnect                                        │
│    ✅ Support multiple devices                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
"""

# ============================================================
# QUICK START: SSH SOCKS5 (5 MENIT SETUP)
# ============================================================

"""
STEP 1: Setup SSH Tunnel (di PC Anda)
--------------------------------------
Windows PowerShell:
    ssh -D 1080 -N user@YOUR_VPS_IP

Linux/Mac:
    ssh -D 1080 -N user@YOUR_VPS_IP

Ganti:
- user: username SSH VPS Anda
- YOUR_VPS_IP: IP address VPS Anda

Masukkan password SSH, tunnel akan jalan di background.


STEP 2: Test Proxy
-------------------
Buka PowerShell baru, test:
    curl --socks5 127.0.0.1:1080 https://api.ipify.org?format=json

Harusnya return IP VPS Anda (bukan IP asli).


STEP 3: Update Python Script
-----------------------------
"""

import requests
from requests.auth import HTTPDigestAuth

# Tambahkan proxies configuration
proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}

url = 'https://development.kiosbank.com:4432/auth/Sign-On'
username = ''
password = '
payload = {
    "mitra": "DJI",
    "accountID": "081310307754",
    "merchantID": "DJI000651",
    "merchantName": "Sinara Artha Mandiri",
    "counterID": "1"
}

# Tambahkan proxies parameter
response = requests.post(
    url,
    auth=HTTPDigestAuth(username, password),
    json=payload,
    proxies=proxies,  # ← TAMBAHKAN INI
    verify=False
)

if response.status_code == 200:
    print("✅ Success!")
    print(f"SessionID: {response.json().get('SessionID')}")
else:
    print(f"❌ Failed: {response.status_code}")
    print(response.text)

"""
STEP 4: Whitelist IP VPS di KIOSBANK
-------------------------------------
1. Login ke dashboard KIOSBANK
2. Masukkan IP VPS Anda (bukan IP PC)
3. Tunggu approval
4. Done!


TIPS:
-----
✅ Keep SSH tunnel running saat development
✅ Untuk auto-reconnect, install autossh:
   
   Windows (via Chocolatey):
   choco install autossh
   
   Linux/Mac:
   apt install autossh  # Ubuntu/Debian
   brew install autossh # Mac
   
   Usage:
   autossh -M 0 -D 1080 -N -f user@YOUR_VPS_IP

✅ Untuk production, upgrade ke Shadowsocks
"""

# ============================================================
# TROUBLESHOOTING
# ============================================================

"""
PROBLEM: "Connection refused" saat SSH tunnel
SOLUTION: 
- Cek SSH service running di VPS: systemctl status ssh
- Cek firewall VPS allow port 22: ufw allow 22


PROBLEM: "SOCKS5 proxy error" di Python
SOLUTION:
- Install PySocks: pip install pysocks
- Atau gunakan requests[socks]: pip install requests[socks]


PROBLEM: Proxy lambat
SOLUTION:
- Cek latency ke VPS: ping YOUR_VPS_IP
- Pilih VPS region yang dekat (Singapore untuk Indonesia)
- Upgrade ke Shadowsocks untuk performance lebih baik


PROBLEM: SSH tunnel sering putus
SOLUTION:
- Gunakan autossh (auto-reconnect)
- Atau upgrade ke Shadowsocks (lebih stabil)
- Set ServerAliveInterval di SSH config:
  
  # ~/.ssh/config
  Host vps
      HostName YOUR_VPS_IP
      User your_user
      ServerAliveInterval 60
      ServerAliveCountMax 3
  
  Lalu connect: ssh -D 1080 -N vps
"""

# ============================================================
# NEXT STEPS
# ============================================================

"""
SETELAH SETUP BERHASIL:
=======================

1. ✅ Whitelist IP VPS di KIOSBANK dashboard
2. ✅ Test Sign-On API dengan script ini
3. ✅ Implement di platform lain (Go, Web, dll)
4. ✅ Untuk production: upgrade ke Shadowsocks
5. ✅ Setup monitoring & auto-restart

DOKUMENTASI LENGKAP:
====================
- SSH SOCKS5: GATEWAY_VPS_SSH_SOCKS5.py
- Shadowsocks: GATEWAY_VPS_SHADOWSOCKS.py

SUPPORT:
========
Jika ada masalah, cek:
1. VPS accessible? → ping YOUR_VPS_IP
2. SSH working? → ssh user@YOUR_VPS_IP
3. Proxy running? → netstat -ano | findstr 1080
4. IP correct? → curl --socks5 127.0.0.1:1080 https://api.ipify.org
"""

print("\n" + "="*60)
print("🚀 VPS Gateway Setup Guide Ready!")
print("="*60)
print("\nQuick Start:")
print("1. ssh -D 1080 -N user@YOUR_VPS_IP")
print("2. Add proxies={'http':'socks5://127.0.0.1:1080',...}")
print("3. Whitelist VPS IP di KIOSBANK")
print("4. Run your script!")
print("="*60)
