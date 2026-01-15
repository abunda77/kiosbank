# ============================================================
# SOLUSI GATEWAY VPS UNTUK DYNAMIC IP
# Multi-Platform Support: Python, Go, Web Browser, dll
# ============================================================

"""
ARSITEKTUR:
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  Your PC    │         │  VPS        │         │  KIOSBANK   │
│ (Dynamic IP)│ ──────> │ (Static IP) │ ──────> │  API Server │
└─────────────┘  SOCKS5 └─────────────┘  HTTPS  └─────────────┘
                Proxy    Whitelist IP

KEUNTUNGAN:
✅ IP Static dari VPS
✅ Support semua platform (Python, Go, Web, Mobile)
✅ Enkripsi otomatis via SSH
✅ Mudah dikonfigurasi
✅ Tidak perlu install software khusus (SSH sudah built-in)
"""

# ============================================================
# OPSI 1: SSH SOCKS5 PROXY (RECOMMENDED - PALING MUDAH)
# ============================================================

"""
SETUP DI VPS (One-time):
------------------------
1. Pastikan SSH server running (biasanya sudah default)
2. Buat user untuk SSH tunnel (opsional, bisa pakai root)
3. Done! Tidak perlu install apapun

SETUP DI PC/LAPTOP:
-------------------
Buka terminal/PowerShell dan jalankan:

Windows PowerShell:
    ssh -D 1080 -N -f user@YOUR_VPS_IP

Linux/Mac:
    ssh -D 1080 -N -f user@YOUR_VPS_IP

Parameter:
- -D 1080    : Buat SOCKS5 proxy di port 1080
- -N         : Tidak execute command (hanya tunnel)
- -f         : Run di background
- user       : Username SSH VPS Anda
- YOUR_VPS_IP: IP VPS Anda

Untuk auto-reconnect jika putus, gunakan autossh:
    autossh -M 0 -D 1080 -N -f user@YOUR_VPS_IP
"""

# ============================================================
# IMPLEMENTASI: PYTHON
# ============================================================

import requests
from requests.auth import HTTPDigestAuth

# Konfigurasi SOCKS5 proxy
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

# Request akan keluar dari IP VPS
response = requests.post(
    url,
    auth=HTTPDigestAuth(username, password),
    json=payload,
    proxies=proxies,  # Route melalui VPS
    verify=False
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

# ============================================================
# IMPLEMENTASI: GO
# ============================================================

"""
package main

import (
    "crypto/tls"
    "fmt"
    "io/ioutil"
    "net/http"
    "net/url"
    "strings"
    
    "golang.org/x/net/proxy"
)

func main() {
    // Setup SOCKS5 proxy
    proxyURL, _ := url.Parse("socks5://127.0.0.1:1080")
    
    // Create SOCKS5 dialer
    dialer, err := proxy.FromURL(proxyURL, proxy.Direct)
    if err != nil {
        panic(err)
    }
    
    // Create HTTP client with SOCKS5 transport
    transport := &http.Transport{
        Dial: dialer.Dial,
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }
    
    client := &http.Client{Transport: transport}
    
    // Make request
    payload := strings.NewReader(`{
        "mitra": "DJI",
        "accountID": "081310307754",
        "merchantID": "DJI000651",
        "merchantName": "Sinara Artha Mandiri",
        "counterID": "1"
    }`)
    
    req, _ := http.NewRequest("POST", 
        "https://development.kiosbank.com:4432/auth/Sign-On", 
        payload)
    
    req.Header.Add("Content-Type", "application/json")
    req.SetBasicAuth("ydn41jme5oc2", "619FDEA9324E5704D1C9C0C062457E08")
    
    resp, err := client.Do(req)
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()
    
    body, _ := ioutil.ReadAll(resp.Body)
    fmt.Println(string(body))
}

// Install dependency:
// go get golang.org/x/net/proxy
"""

# ============================================================
# IMPLEMENTASI: WEB BROWSER (Chrome/Firefox)
# ============================================================

"""
CHROME:
-------
1. Install extension: "Proxy SwitchyOmega"
2. Konfigurasi:
   - Protocol: SOCKS5
   - Server: 127.0.0.1
   - Port: 1080
3. Aktifkan profile proxy
4. Buka web app Anda, semua request via VPS

FIREFOX:
--------
Settings → Network Settings → Manual proxy configuration
- SOCKS Host: 127.0.0.1
- Port: 1080
- SOCKS v5: ✓
- Proxy DNS when using SOCKS v5: ✓

SYSTEM-WIDE (Windows):
----------------------
Settings → Network & Internet → Proxy → Manual proxy setup
- Use a proxy server: ON
- Address: socks5://127.0.0.1
- Port: 1080
"""

# ============================================================
# IMPLEMENTASI: cURL (untuk testing)
# ============================================================

"""
curl --socks5 127.0.0.1:1080 \
     --digest -u "ydn41jme5oc2:619FDEA9324E5704D1C9C0C062457E08" \
     -H "Content-Type: application/json" \
     -d '{"mitra":"DJI","accountID":"081310307754","merchantID":"DJI000651","merchantName":"Sinara Artha Mandiri","counterID":"1"}' \
     -k \
     https://development.kiosbank.com:4432/auth/Sign-On
"""

print("\n✅ SSH SOCKS5 Proxy Configuration Complete!")
