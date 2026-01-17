# ============================================================
# SETUP GUIDE - VPS Gateway untuk KIOSBANK API
# VPS: 193.219.97.148 (alwyzon)
# ============================================================

"""
LANGKAH-LANGKAH SETUP:
======================

STEP 1: Update Whitelist di KIOSBANK Dashboard
-----------------------------------------------
1. Login ke dashboard KIOSBANK
2. Ganti IP whitelist dari: 103.3.220.101
   Menjadi: 193.219.97.148 (IP VPS Anda)
3. Kategori: Development
4. Tunggu approval


STEP 2: Start SSH Tunnel
-------------------------
Pilih salah satu cara:

CARA A - Menggunakan Batch File (Recommended):
   Double-click file: start_ssh_tunnel.bat
   
CARA B - Manual via PowerShell:
   ssh -D 1080 -N alwyzon@193.219.97.148

Masukkan password SSH VPS Anda saat diminta.
PENTING: Biarkan window ini tetap TERBUKA!


STEP 3: Verify Proxy Working
-----------------------------
Buka PowerShell baru (jangan tutup SSH tunnel), jalankan:

   curl --socks5 127.0.0.1:1080 https://api.ipify.org?format=json

Expected output:
   {"ip":"193.219.97.148"}

Jika IP yang muncul adalah 193.219.97.148 → ✅ Proxy berhasil!


STEP 4: Install Python Dependencies
------------------------------------
   pip install requests pysocks urllib3


STEP 5: Test KIOSBANK API
--------------------------
   python signon_vps.py

Expected output jika berhasil:
   ============================================================
   VPS GATEWAY CONFIGURATION
   ============================================================
   VPS IP: 193.219.97.148
   VPS User: alwyzon
   🔒 Using SOCKS5 proxy: 127.0.0.1:1080
   ============================================================
   
   📡 Checking proxy connection...
   ✅ Proxy working!
      Your outgoing IP: 193.219.97.148
      ✓✓ PERFECT! IP matches VPS IP (193.219.97.148)
   
   ============================================================
   KIOSBANK Sign-On Request
   ============================================================
   
   ✅✅ SIGN-ON SUCCESSFUL!
   ============================================================
   SessionID: 48cb1cf1b5f04234113720662f3120c0
   ============================================================


TROUBLESHOOTING:
================

Problem: "Connection refused" saat SSH
Solution:
   1. Cek SSH service di VPS:
      ssh alwyzon@193.219.97.148
      systemctl status ssh
   
   2. Cek firewall VPS:
      sudo ufw status
      sudo ufw allow 22


Problem: "Proxy error" di Python
Solution:
   1. Pastikan SSH tunnel masih running
   2. Cek proxy listening:
      netstat -ano | findstr 1080
   
   3. Install PySocks jika belum:
      pip install pysocks


Problem: "404 Not Found" dari KIOSBANK
Solution:
   1. VPS IP belum di-whitelist
   2. Tunggu approval dari tim KIOSBANK
   3. Verify IP yang keluar:
      curl --socks5 127.0.0.1:1080 https://api.ipify.org


Problem: SSH tunnel sering putus
Solution:
   Install autossh untuk auto-reconnect:
   
   Windows (via Chocolatey):
      choco install autossh
   
   Usage:
      autossh -M 0 -D 1080 -N -f alwyzon@193.219.97.148


TIPS & BEST PRACTICES:
======================

1. Keep SSH tunnel running saat development
   - Jangan tutup window SSH tunnel
   - Atau gunakan autossh untuk auto-reconnect

2. Untuk production, upgrade ke Shadowsocks
   - Lebih stabil dan cepat
   - Auto-reconnect built-in
   - Lihat: GATEWAY_VPS_SHADOWSOCKS.py

3. Monitor koneksi
   - Cek proxy: netstat -ano | findstr 1080
   - Cek IP: curl --socks5 127.0.0.1:1080 https://api.ipify.org

4. Security
   - Gunakan SSH key authentication (lebih aman dari password)
   - Setup fail2ban di VPS untuk protect SSH
   - Update VPS regularly: sudo apt update && sudo apt upgrade


MULTI-PLATFORM USAGE:
=====================

Setelah SSH tunnel running, semua aplikasi bisa pakai proxy:

Python:
   proxies = {
       'http': 'socks5://127.0.0.1:1080',
       'https': 'socks5://127.0.0.1:1080'
   }

Go:
   proxyURL, _ := url.Parse("socks5://127.0.0.1:1080")
   dialer, _ := proxy.FromURL(proxyURL, proxy.Direct)

cURL:
   curl --socks5 127.0.0.1:1080 [URL]

Chrome/Firefox:
   Install extension: Proxy SwitchyOmega
   Configure: SOCKS5, 127.0.0.1:1080


FILES REFERENCE:
================

start_ssh_tunnel.bat    → Start SSH tunnel (double-click)
signon_vps.py          → Test KIOSBANK API dengan proxy
README_VPS_GATEWAY.md  → Dokumentasi lengkap
GATEWAY_VPS_SSH_SOCKS5.py     → SSH SOCKS5 documentation
GATEWAY_VPS_SHADOWSOCKS.py    → Shadowsocks documentation (production)


NEXT STEPS AFTER SUCCESS:
==========================

1. ✅ Test semua API endpoints KIOSBANK
2. ✅ Implement di aplikasi production Anda
3. ✅ Setup monitoring & logging
4. ✅ Consider upgrade ke Shadowsocks untuk production
5. ✅ Setup backup VPS atau multiple VPS untuk redundancy


SUPPORT:
========

Jika masih ada masalah:
1. Cek VPS accessible: ping 193.219.97.148
2. Cek SSH working: ssh alwyzon@193.219.97.148
3. Cek proxy running: netstat -ano | findstr 1080
4. Cek IP correct: curl --socks5 127.0.0.1:1080 https://api.ipify.org
5. Cek whitelist: Login KIOSBANK dashboard


Good luck! 🚀
"""

print(__doc__)
