# 📚 KIOSBANK Project - File Summary

## 🎯 Overview

Project KIOSBANK Management Console memiliki 2 versi:
1. **GUI Version** (`main.py`) - Untuk desktop/komputer lokal dengan Tkinter
2. **CLI Version** (`main_cli.py`) - Untuk VPS headless dengan text-based interface

---

## 📁 File Structure

```
kisobank/
├── main.py                    # GUI version (Tkinter) - untuk desktop
├── main_cli.py                # CLI version - untuk VPS headless
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (JANGAN di-commit!)
├── .env.example              # Template untuk .env
├── .gitignore                # Git ignore rules
│
├── 📖 Documentation
│   ├── README.md             # Project overview
│   ├── CLI_GUIDE.md          # CLI version usage guide
│   ├── VPS_DEPLOYMENT.md     # VPS deployment guide
│   ├── QUICKSTART.md         # Quick start guide
│   ├── SECURITY.md           # Security guidelines
│   └── MIGRATION_SUMMARY.md  # Migration to .env guide
│
├── 🚀 Deployment
│   └── deploy_vps.sh         # Automated VPS deployment script
│
├── 📂 app/                   # Application scripts
│   ├── signon_vps.py         # Sign-on to KIOSBANK API
│   ├── start_ssh_tunnel.py   # Start SSH SOCKS5 tunnel
│   ├── check_ip.py           # Check public IP address
│   ├── cekport_gui.py        # Check port status
│   ├── verify_env.py         # Verify .env configuration
│   ├── env_config.py         # Environment config loader
│   └── ...                   # Other utility scripts
│
└── 📂 db/                    # Database related files
    ├── db_helper.py          # Database helper functions
    ├── ppob.db               # SQLite database
    └── ...                   # Other DB files
```

---

## 🎮 Usage Guide

### For Desktop (Windows/Linux with GUI)

```bash
# Run GUI version
python main.py
```

**Features:**
- ✅ Beautiful Tkinter interface
- ✅ Real-time output in scrolled text widget
- ✅ Colored syntax highlighting
- ✅ Stop button for running processes
- ✅ Concurrent script execution support

### For VPS (Headless Linux Server)

```bash
# Run CLI version
python3 main_cli.py
```

**Features:**
- ✅ Interactive text-based menu
- ✅ ANSI colored output
- ✅ Real-time script execution
- ✅ System information display
- ✅ Keyboard interrupt handling

---

## 📋 Available Scripts

### Core Operations

| Script | Description | Usage |
|--------|-------------|-------|
| `app/signon_vps.py` | Establish session with KIOSBANK API | `python3 app/signon_vps.py` |
| `app/start_ssh_tunnel.py` | Start SSH SOCKS5 tunnel to VPS | `python3 app/start_ssh_tunnel.py` |

### Diagnostics & Checks

| Script | Description | Usage |
|--------|-------------|-------|
| `app/check_ip.py` | Verify current public IP | `python3 app/check_ip.py` |
| `app/cekport_gui.py` | Analyze open ports & proxy | `python3 app/cekport_gui.py` |
| `app/verify_env.py` | Validate .env configuration | `python3 app/verify_env.py` |

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# VPS Configuration
VPS_IP=your_vps_ip
VPS_USER=your_username

# Proxy Configuration
USE_PROXY=True
PROXY_HOST=127.0.0.1
PROXY_PORT=1080

# KIOSBANK API
KIOSBANK_API_URL=https://api.kiosbank.com/endpoint
KIOSBANK_API_USERNAME=your_username
KIOSBANK_API_PASSWORD=your_password

# Payload
KIOSBANK_MITRA=your_mitra
KIOSBANK_ACCOUNT_ID=your_account_id
KIOSBANK_MERCHANT_ID=your_merchant_id
KIOSBANK_MERCHANT_NAME=your_merchant_name
KIOSBANK_COUNTER_ID=your_counter_id

# Registered IP
REGISTERED_IP=your_registered_ip
```

---

## 📦 Dependencies

Install dengan: `pip install -r requirements.txt`

- **requests** - HTTP requests ke API
- **urllib3** - SSL/TLS handling
- **PySocks** - SOCKS5 proxy support
- **typing-extensions** - Type hints support

**Built-in modules** (tidak perlu install):
- tkinter (GUI version)
- sqlite3 (database)
- subprocess, threading, queue, sys, os, platform, datetime

---

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone/download project
cd /path/to/kisobank

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
nano .env  # Edit dengan credentials Anda

# 4. Verify configuration
python app/verify_env.py

# 5. Run GUI application
python main.py
```

### VPS Deployment

```bash
# 1. Upload to VPS
scp -r kisobank user@vps-ip:/home/user/

# 2. SSH to VPS
ssh user@vps-ip

# 3. Run deployment script
cd ~/kisobank
chmod +x deploy_vps.sh
./deploy_vps.sh

# 4. Configure .env
nano .env

# 5. Run CLI application
python3 main_cli.py
```

---

## 🆚 GUI vs CLI Comparison

| Feature | GUI (`main.py`) | CLI (`main_cli.py`) |
|---------|----------------|-------------------|
| **Platform** | Desktop with GUI | VPS headless / Terminal |
| **Interface** | Tkinter windows | Text-based menu |
| **Colors** | Widget styling | ANSI color codes |
| **Output** | ScrolledText widget | Terminal stdout |
| **Concurrent** | Multi-threading support | Sequential execution |
| **Stop** | Stop button | Ctrl+C interrupt |
| **Best For** | Local development | Production VPS |

---

## 🔐 Security Notes

1. **Never commit .env file** to Git
2. **Set proper file permissions**: `chmod 600 .env`
3. **Use SSH key authentication** for VPS
4. **Enable firewall** on VPS
5. **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| `CLI_GUIDE.md` | Comprehensive CLI usage guide |
| `VPS_DEPLOYMENT.md` | Step-by-step VPS deployment |
| `QUICKSTART.md` | Quick start for beginners |
| `SECURITY.md` | Security best practices |
| `MIGRATION_SUMMARY.md` | Migration to .env guide |

---

## 🐛 Common Issues

### GUI tidak muncul di VPS
**Problem:** Tkinter membutuhkan display server  
**Solution:** Gunakan `main_cli.py` untuk VPS headless

### Module not found
**Problem:** Dependencies belum terinstall  
**Solution:** `pip install -r requirements.txt`

### Permission denied
**Problem:** File tidak executable  
**Solution:** `chmod +x main_cli.py`

### Colors tidak muncul
**Problem:** Terminal tidak support ANSI colors  
**Solution:** Gunakan terminal modern atau set `TERM=xterm-256color`

---

## 📞 Support

Untuk bantuan lebih lanjut:
1. Baca dokumentasi di folder docs
2. Check troubleshooting section di VPS_DEPLOYMENT.md
3. Review error logs
4. Hubungi tim development

---

**Last Updated:** 2026-01-17  
**Version:** 2.0 (CLI Support Added)
