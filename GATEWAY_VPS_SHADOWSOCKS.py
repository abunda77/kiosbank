# ============================================================
# OPSI 2: SHADOWSOCKS (LEBIH CEPAT, LEBIH STABIL)
# Cocok untuk production & high-traffic
# ============================================================

"""
KELEBIHAN SHADOWSOCKS vs SSH:
✅ Performance lebih baik (optimized untuk proxy)
✅ Lebih stabil untuk koneksi long-running
✅ Support multiple users/devices
✅ Auto-reconnect built-in
✅ Lebih ringan resource VPS

KEKURANGAN:
⚠️ Perlu install software di VPS & client
⚠️ Setup sedikit lebih kompleks (tapi masih mudah)
"""

# ============================================================
# SETUP SHADOWSOCKS DI VPS (Ubuntu/Debian)
# ============================================================

"""
1. SSH ke VPS Anda:
   ssh root@YOUR_VPS_IP

2. Install Shadowsocks-libev (versi paling cepat):
   
   # Update package list
   apt update
   
   # Install shadowsocks-libev
   apt install shadowsocks-libev -y

3. Konfigurasi Shadowsocks:
   
   nano /etc/shadowsocks-libev/config.json
   
   Isi dengan:
   {
       "server": "0.0.0.0",
       "server_port": 8388,
       "password": "GANTI_PASSWORD_KUAT_ANDA",
       "timeout": 300,
       "method": "chacha20-ietf-poly1305",
       "mode": "tcp_and_udp",
       "fast_open": true
   }
   
   Tips password: gunakan password yang kuat, misal:
   openssl rand -base64 32

4. Start Shadowsocks service:
   
   systemctl enable shadowsocks-libev
   systemctl start shadowsocks-libev
   systemctl status shadowsocks-libev
   
5. Buka firewall (jika ada):
   
   ufw allow 8388/tcp
   ufw allow 8388/udp

6. Verify service running:
   
   netstat -tulpn | grep 8388
   
   Seharusnya muncul: 0.0.0.0:8388

✅ SETUP VPS SELESAI!
"""

# ============================================================
# SETUP CLIENT DI WINDOWS
# ============================================================

"""
METODE 1: Shadowsocks GUI Client (Paling Mudah)
------------------------------------------------

1. Download Shadowsocks Windows Client:
   https://github.com/shadowsocks/shadowsocks-windows/releases
   
   File: Shadowsocks-x.x.x.zip

2. Extract dan jalankan Shadowsocks.exe

3. Konfigurasi:
   - Server Address: YOUR_VPS_IP
   - Server Port: 8388
   - Password: PASSWORD_YANG_ANDA_SET
   - Encryption: chacha20-ietf-poly1305
   - Local Port: 1080 (SOCKS5)

4. Klik "Enable System Proxy" atau "PAC Mode"

5. Done! Semua aplikasi akan route via VPS


METODE 2: Command Line (untuk automation)
------------------------------------------

1. Download shadowsocks-rust (lebih cepat):
   https://github.com/shadowsocks/shadowsocks-rust/releases
   
   File: shadowsocks-vX.X.X.x86_64-pc-windows-msvc.zip

2. Extract ke folder, misal: C:\shadowsocks

3. Buat config file: config.json
   {
       "server": "YOUR_VPS_IP",
       "server_port": 8388,
       "password": "PASSWORD_ANDA",
       "method": "chacha20-ietf-poly1305",
       "local_address": "127.0.0.1",
       "local_port": 1080
   }

4. Jalankan:
   sslocal.exe -c config.json

5. SOCKS5 proxy ready di 127.0.0.1:1080
"""

# ============================================================
# IMPLEMENTASI: PYTHON dengan Shadowsocks
# ============================================================

import requests
from requests.auth import HTTPDigestAuth

# Shadowsocks SOCKS5 proxy (sama seperti SSH)
proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}

url = 'https://development.kiosbank.com:4432/auth/Sign-On'
username = 'ydn41jme5oc2'
password = '619FDEA9324E5704D1C9C0C062457E08'
payload = {
    "mitra": "DJI",
    "accountID": "081310307754",
    "merchantID": "DJI000651",
    "merchantName": "Sinara Artha Mandiri",
    "counterID": "1"
}

response = requests.post(
    url,
    auth=HTTPDigestAuth(username, password),
    json=payload,
    proxies=proxies,
    verify=False
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

# ============================================================
# AUTO-START SHADOWSOCKS CLIENT (Windows)
# ============================================================

"""
Agar Shadowsocks auto-start saat Windows boot:

1. Buat file: start_shadowsocks.bat
   
   @echo off
   cd C:\shadowsocks
   start /min sslocal.exe -c config.json

2. Tekan Win+R, ketik: shell:startup

3. Copy start_shadowsocks.bat ke folder startup

4. Done! Shadowsocks akan auto-start setiap boot
"""

# ============================================================
# MONITORING & TROUBLESHOOTING
# ============================================================

"""
CEK KONEKSI KE VPS:
-------------------
# Windows PowerShell
Test-NetConnection -ComputerName YOUR_VPS_IP -Port 8388

# Linux/Mac
nc -zv YOUR_VPS_IP 8388

CEK SHADOWSOCKS CLIENT RUNNING:
--------------------------------
# Windows
netstat -ano | findstr 1080

# Linux/Mac
lsof -i :1080

TEST PROXY:
-----------
# Via curl
curl --socks5 127.0.0.1:1080 https://api.ipify.org?format=json

# Seharusnya return IP VPS Anda, bukan IP asli

COMMON ISSUES:
--------------
1. Connection refused → VPS firewall blocking port 8388
2. Authentication failed → Password salah
3. Timeout → VPS down atau network issue
"""

print("\n✅ Shadowsocks Configuration Complete!")
