"""
SOLUSI DYNAMIC IP: Menggunakan VPS sebagai Proxy

Arsitektur:
[Your PC (Dynamic IP)] --> [VPS (Static IP)] --> [KIOSBANK API]

Langkah-langkah:
1. Sewa VPS murah (DigitalOcean, Vultr, AWS Lightsail, dll)
   - Biaya: ~$5-10/bulan (~Rp 75k-150k)
   - Dapat IP static yang tidak berubah

2. Install proxy di VPS (contoh: Nginx, SSH Tunnel, atau Wireguard VPN)

3. Whitelist IP VPS di dashboard KIOSBANK

4. Semua request dari PC Anda route melalui VPS

CONTOH IMPLEMENTASI:
"""

# ============================================================
# OPSI A: SSH Tunnel (Paling Mudah)
# ============================================================
# Di PC Anda, buat SSH tunnel ke VPS:
# ssh -D 8080 user@your-vps-ip

# Lalu gunakan SOCKS proxy di Python:
import requests
from requests.auth import HTTPDigestAuth
from env_config import get_env, get_env_int

# Load configuration from environment variables
proxies = {
    'http': f'socks5://{get_env("PROXY_HOST", default="127.0.0.1")}:{get_env_int("PROXY_PORT", default=8080)}',
    'https': f'socks5://{get_env("PROXY_HOST", default="127.0.0.1")}:{get_env_int("PROXY_PORT", default=8080)}'
}

url = get_env('KIOSBANK_API_URL', required=True)
username = get_env('KIOSBANK_API_USERNAME', required=True)
password = get_env('KIOSBANK_API_PASSWORD', required=True)
payload = {
    "mitra": get_env('KIOSBANK_MITRA', required=True),
    "accountID": get_env('KIOSBANK_ACCOUNT_ID', required=True),
    "merchantID": get_env('KIOSBANK_MERCHANT_ID', required=True),
    "merchantName": get_env('KIOSBANK_MERCHANT_NAME', required=True),
    "counterID": get_env('KIOSBANK_COUNTER_ID', required=True)
}

# Request akan keluar dari IP VPS
response = requests.post(
    url,
    auth=HTTPDigestAuth(username, password),
    json=payload,
    proxies=proxies,  # Route through VPS
    verify=False
)

# ============================================================
# OPSI B: Wireguard VPN (Lebih Aman)
# ============================================================
# 1. Install Wireguard di VPS
# 2. Install Wireguard client di PC
# 3. Semua traffic otomatis route via VPS
# 4. Tidak perlu ubah code Python

print("VPS Proxy Solution Ready!")
