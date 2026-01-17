# VPS Gateway untuk KIOSBANK API - Complete Guide

## 📋 Daftar Isi
1. [Ringkasan Solusi](#ringkasan-solusi)
2. [Quick Start (5 Menit)](#quick-start-5-menit)
3. [Setup Detail](#setup-detail)
4. [Multi-Platform Implementation](#multi-platform-implementation)
5. [Troubleshooting](#troubleshooting)

---

## 🎯 Ringkasan Solusi

### Problem
- IP Anda **dynamic** dari ISP (berubah-ubah)
- KIOSBANK API memerlukan **IP whitelist**
- Butuh solusi yang **multi-platform** (Python, Go, Web, dll)

### Solution
Gunakan **VPS sebagai gateway** dengan IP static:

```
[PC/Laptop]  ──SOCKS5──>  [VPS]  ──HTTPS──>  [KIOSBANK API]
(Dynamic IP)              (Static IP - Whitelisted)
```

### Pilihan Teknologi

| Solusi | Setup Time | Kecepatan | Rekomendasi |
|--------|------------|-----------|-------------|
| **SSH SOCKS5** | 5 menit | ⭐⭐⭐⭐ | ✅ Start here |
| **Shadowsocks** | 15 menit | ⭐⭐⭐⭐⭐ | ✅ Production |

---

## 🚀 Quick Start (5 Menit)

### Prerequisites
- ✅ VPS dengan SSH access (Ubuntu/Debian recommended)
- ✅ IP VPS sudah di-whitelist di KIOSBANK dashboard

### Step 1: Start SSH Tunnel

**Windows PowerShell:**
```powershell
ssh -D 1080 -N user@YOUR_VPS_IP
```

**Linux/Mac:**
```bash
ssh -D 1080 -N user@YOUR_VPS_IP
```

Ganti:
- `user` → username SSH VPS Anda
- `YOUR_VPS_IP` → IP address VPS Anda

> 💡 Biarkan terminal ini tetap terbuka!

### Step 2: Test Proxy

Buka terminal/PowerShell baru:

```powershell
curl --socks5 127.0.0.1:1080 https://api.ipify.org?format=json
```

**Expected output:**
```json
{"ip":"YOUR_VPS_IP"}
```

✅ Jika IP yang muncul adalah IP VPS → Proxy berhasil!

### Step 3: Install Python Dependencies

```bash
pip install requests pysocks
```

### Step 4: Run Script

```bash
python signon_with_proxy.py
```

**Expected output jika berhasil:**
```
🔒 Using SOCKS5 proxy: 127.0.0.1:1080
📡 Checking proxy connection...
✅ Proxy working! Your IP: YOUR_VPS_IP

============================================================
KIOSBANK Sign-On Request
============================================================
✅✅ SIGN-ON SUCCESSFUL!
============================================================
SessionID: 48cb1cf1b5f04234113720662f3120c0
============================================================
```

---

## 📚 Setup Detail

### A. SSH SOCKS5 (Recommended untuk Start)

#### Kelebihan:
- ✅ Setup super cepat (5 menit)
- ✅ Tidak perlu install software tambahan
- ✅ Enkripsi built-in (via SSH)
- ✅ Works out of the box

#### Kekurangan:
- ⚠️ Koneksi bisa putus jika network unstable
- ⚠️ Perlu manual restart jika putus

#### Auto-Reconnect (Recommended)

**Install autossh:**

Windows (via Chocolatey):
```powershell
choco install autossh
```

Linux:
```bash
sudo apt install autossh
```

Mac:
```bash
brew install autossh
```

**Usage:**
```bash
autossh -M 0 -D 1080 -N -f user@YOUR_VPS_IP
```

Parameter:
- `-M 0` → Monitoring port (0 = auto)
- `-D 1080` → SOCKS5 proxy port
- `-N` → No command execution
- `-f` → Background mode

---

### B. Shadowsocks (Recommended untuk Production)

#### Kelebihan:
- ✅ Performance lebih baik
- ✅ Auto-reconnect built-in
- ✅ Lebih stabil untuk long-running
- ✅ Support multiple devices

#### Setup VPS (Ubuntu/Debian):

```bash
# 1. SSH ke VPS
ssh root@YOUR_VPS_IP

# 2. Install Shadowsocks
apt update
apt install shadowsocks-libev -y

# 3. Konfigurasi
nano /etc/shadowsocks-libev/config.json
```

**config.json:**
```json
{
    "server": "0.0.0.0",
    "server_port": 8388,
    "password": "GANTI_PASSWORD_KUAT_ANDA",
    "timeout": 300,
    "method": "chacha20-ietf-poly1305",
    "mode": "tcp_and_udp",
    "fast_open": true
}
```

Generate password kuat:
```bash
openssl rand -base64 32
```

```bash
# 4. Start service
systemctl enable shadowsocks-libev
systemctl start shadowsocks-libev

# 5. Buka firewall
ufw allow 8388/tcp
ufw allow 8388/udp

# 6. Verify
systemctl status shadowsocks-libev
netstat -tulpn | grep 8388
```

#### Setup Client (Windows):

**Download Shadowsocks Client:**
- GUI: https://github.com/shadowsocks/shadowsocks-windows/releases
- CLI: https://github.com/shadowsocks/shadowsocks-rust/releases

**Konfigurasi:**
- Server: YOUR_VPS_IP
- Port: 8388
- Password: (password yang Anda set)
- Encryption: chacha20-ietf-poly1305
- Local Port: 1080

**Start client** → SOCKS5 proxy ready di `127.0.0.1:1080`

---

## 💻 Multi-Platform Implementation

### Python

```python
import requests
from requests.auth import HTTPDigestAuth

proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}

response = requests.post(
    'https://development.kiosbank.com:4432/auth/Sign-On',
    auth=HTTPDigestAuth('username', 'password'),
    json=payload,
    proxies=proxies,
    verify=False
)
```

### Go

```go
package main

import (
    "golang.org/x/net/proxy"
    "net/http"
    "net/url"
)

func main() {
    // Setup SOCKS5
    proxyURL, _ := url.Parse("socks5://127.0.0.1:1080")
    dialer, _ := proxy.FromURL(proxyURL, proxy.Direct)
    
    transport := &http.Transport{Dial: dialer.Dial}
    client := &http.Client{Transport: transport}
    
    // Make request
    resp, _ := client.Post("https://development.kiosbank.com:4432/auth/Sign-On", ...)
}
```

### cURL

```bash
curl --socks5 127.0.0.1:1080 \
     --digest -u "username:password" \
     -H "Content-Type: application/json" \
     -d '{"mitra":"DJI",...}' \
     -k \
     https://development.kiosbank.com:4432/auth/Sign-On
```

### Web Browser (Chrome)

1. Install extension: **Proxy SwitchyOmega**
2. Konfigurasi:
   - Protocol: SOCKS5
   - Server: 127.0.0.1
   - Port: 1080
3. Aktifkan proxy
4. Semua web request via VPS

---

## 🔧 Troubleshooting

### Problem: "Connection refused" saat SSH tunnel

**Solution:**
```bash
# Cek SSH service di VPS
ssh user@YOUR_VPS_IP
systemctl status ssh

# Cek firewall
ufw allow 22
```

### Problem: "SOCKS5 proxy error" di Python

**Solution:**
```bash
# Install PySocks
pip install pysocks

# Atau
pip install requests[socks]
```

### Problem: Proxy lambat

**Solution:**
- Pilih VPS region dekat (Singapore untuk Indonesia)
- Upgrade ke Shadowsocks (lebih cepat)
- Cek latency: `ping YOUR_VPS_IP`

### Problem: SSH tunnel sering putus

**Solution:**
- Gunakan `autossh` (auto-reconnect)
- Atau upgrade ke Shadowsocks
- Edit SSH config:

```bash
# ~/.ssh/config
Host vps
    HostName YOUR_VPS_IP
    User your_user
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### Problem: "IP not whitelisted"

**Solution:**
1. Verify IP VPS di dashboard KIOSBANK
2. Test IP yang keluar:
   ```bash
   curl --socks5 127.0.0.1:1080 https://api.ipify.org
   ```
3. Pastikan IP match dengan yang di-whitelist

---

## 📊 Monitoring

### Cek Proxy Running

**Windows:**
```powershell
netstat -ano | findstr 1080
```

**Linux/Mac:**
```bash
lsof -i :1080
```

### Cek IP yang Keluar

```bash
curl --socks5 127.0.0.1:1080 https://api.ipify.org?format=json
```

### Monitor Shadowsocks (VPS)

```bash
# Status service
systemctl status shadowsocks-libev

# Logs
journalctl -u shadowsocks-libev -f

# Connection count
netstat -an | grep 8388 | wc -l
```

---

## 🎯 Best Practices

### Development
- ✅ Gunakan SSH SOCKS5 (simple & cepat)
- ✅ Keep terminal SSH tunnel tetap open
- ✅ Test dengan `signon_with_proxy.py`

### Production
- ✅ Upgrade ke Shadowsocks (lebih stabil)
- ✅ Setup auto-start client
- ✅ Monitor VPS uptime
- ✅ Backup VPS configuration

### Security
- ✅ Gunakan password kuat untuk Shadowsocks
- ✅ Jangan expose port Shadowsocks ke public (gunakan firewall)
- ✅ Update VPS regularly: `apt update && apt upgrade`
- ✅ Setup fail2ban untuk SSH protection

---

## 📁 File Reference

| File | Deskripsi |
|------|-----------|
| `signon_with_proxy.py` | Production-ready script dengan proxy |
| `QUICK_START_VPS_GATEWAY.py` | Quick start guide |
| `GATEWAY_VPS_SSH_SOCKS5.py` | SSH SOCKS5 documentation |
| `GATEWAY_VPS_SHADOWSOCKS.py` | Shadowsocks documentation |

---

## 🆘 Support

Jika masih ada masalah, cek:

1. ✅ VPS accessible? → `ping YOUR_VPS_IP`
2. ✅ SSH working? → `ssh user@YOUR_VPS_IP`
3. ✅ Proxy running? → `netstat -ano | findstr 1080`
4. ✅ IP correct? → `curl --socks5 127.0.0.1:1080 https://api.ipify.org`
5. ✅ VPS IP whitelisted? → Check KIOSBANK dashboard

---

**Good luck! 🚀**
